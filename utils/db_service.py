import time
from datetime import datetime
import sqlite3
import bcrypt


class DBService(object):
    def __init__(self):
        self.conn = sqlite3.connect('./db/database.db')
        self.cur = self.conn.cursor()

    # 初始化数据库，创建表，没有表则创建
    def init_db(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS role (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL,
                            is_admin BOOLEAN NOT NULL
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_id INTEGER NOT NULL,
                            group_name TEXT NOT NULL
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS activities (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            capacity INTEGER NOT NULL,
                            enrolled INTEGER NOT NULL,
                            startTime TIMESTAMP NOT NULL,
                            endTime TIMESTAMP NOT NULL,
                            title TEXT NOT NULL,
                            status TEXT NOT NULL,
                            description TEXT NOT NULL,
                            department TEXT NOT NULL,
                            cover TEXT NOT NULL,
                            location TEXT NOT NULL,
                            registration_time TIMESTAMP NOT NULL
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS signup (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            activity_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        self.conn.commit()

    def add_user(self, username, password, name):
        is_insert = self.conn.execute("SELECT * FROM users WHERE username =?", (username,)).fetchone()
        if is_insert is None:
            hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            self.conn.execute("INSERT INTO users (username, password, name) VALUES (?,?,?)", (username, hashed_password, name))
            self.conn.commit()

    def get_password(self, username):
        self.cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        db_pwd = self.cur.fetchone()
        if db_pwd:
            return db_pwd[0]
        else:
            return None

    def get_user_id(self, username):
        self.cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        db_id = self.cur.fetchone()
        if db_id:
            return db_id[0]
        else:
            return None

    def get_all_users(self):
        # 联合查询users和role和groups表，获取所有用户信息
        self.cur.execute("SELECT users.id, users.username, users.created_at, groups.id, role.is_admin, users.name FROM users INNER JOIN role ON users.id = role.user_id INNER JOIN groups ON role.group_id = groups.id")
        users = self.cur.fetchall()
        return users

    def create_user(self, department, username, password, name, is_admin=False):
        self.add_user(username, password, name)
        user_id = self.get_user_id(username)
        self.cur.execute("INSERT INTO role (user_id, group_id, is_admin) VALUES (?,?,?)", (user_id, department, is_admin))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.cur.execute("DELETE FROM role WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def reset_password(self, user_id):
        password = bcrypt.hashpw(b"123456", bcrypt.gensalt())
        self.cur.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))
        self.conn.commit()

    def create_activity(self, capacity, enrolled, start_time, end_time, title, status, description, department, cover,
                        location, registration_time):
        self.cur.execute("INSERT INTO activities (capacity, enrolled, startTime, endTime, title, status, description, department, cover, location, registration_time) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (capacity, enrolled, start_time, end_time, title, status, description, department, cover, location, registration_time))
        self.conn.commit()

    def get_user_info(self, user_id):
        self.cur.execute("SELECT users.username, role.is_admin FROM users INNER JOIN role ON users.id = role.user_id WHERE users.id = ?", (user_id,))
        user_info = self.cur.fetchone()
        return user_info

    def enroll_activity(self, active_id, user_id):
        self.check_activity_status(active_id)
        is_start = self.cur.execute("SELECT registration_time, status FROM activities WHERE id = ?", (active_id,)).fetchall()
        if is_start is None:
            return None
        now_time = time.time()
        # 2025-05-02T00:00:00+08:00
        if now_time < datetime.strptime(is_start[0][0], '%Y-%m-%dT%H:%M:%S%z').timestamp() or is_start[0][1] != 'upcoming':
            return None

        is_insert = self.conn.execute("SELECT * FROM signup WHERE user_id =? AND activity_id =?", (user_id, active_id)).fetchone()
        if is_insert is None:
            # 报名人数不超过上限，则插入报名表，报名人数+1
            enrolled_num = self.cur.execute("SELECT enrolled, capacity FROM activities WHERE id = ?", (active_id,)).fetchone()
            if enrolled_num[0] < enrolled_num[1]:
                self.cur.execute("UPDATE activities SET enrolled = enrolled + 1 WHERE id = ?", (active_id,))
                self.cur.execute("INSERT INTO signup (user_id, activity_id) VALUES (?,?)", (user_id, active_id))
                self.conn.commit()

    def get_activities(self, user_id):
        activity_ids = self.cur.execute("SELECT id FROM activities").fetchall()
        for i in activity_ids:
            self.check_activity_status(i)
        department = self.cur.execute("SELECT group_id FROM role WHERE user_id = ?", (user_id,)).fetchone()
        if department is None:
            return []
        department_text = self.cur.execute("SELECT group_name FROM groups WHERE id = ?", (department[0],)).fetchone()
        self.cur.execute("SELECT activities.id, activities.title, activities.status, activities.startTime, activities.endTime, activities.description, activities.department, activities.cover, activities.location , activities.enrolled, activities.capacity, activities.registration_time FROM activities")
        activities = self.cur.fetchall()
        return activities, department_text

    def get_user_activity_info(self, user_id):
        all_signed_activity_ids = self.cur.execute("SELECT activity_id FROM signup WHERE user_id = ?", (user_id,)).fetchone()
        if all_signed_activity_ids is None:
            return []
        for i in all_signed_activity_ids:
            self.check_activity_status(i)
        self.cur.execute("SELECT activities.id, activities.title, activities.status, activities.startTime, activities.endTime, activities.description, activities.department, activities.cover, activities.location , activities.enrolled, activities.capacity FROM activities WHERE id IN ({})".format(','.join('?' * len(all_signed_activity_ids))), all_signed_activity_ids)
        activities = self.cur.fetchall()
        return activities

    def cancel_enroll_activity(self, active_id, user_id):
        self.check_activity_status(active_id)
        self.cur.execute("DELETE FROM signup WHERE user_id = ? AND activity_id = ?", (user_id, active_id))
        self.cur.execute("UPDATE activities SET enrolled = enrolled - 1 WHERE id = ?", (active_id,))
        self.conn.commit()

    def delete_activity(self, activity_id):
        self.cur.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        self.cur.execute("DELETE FROM signup WHERE activity_id = ?", (activity_id,))
        self.conn.commit()

    def is_admin(self, user_id):
        self.cur.execute("SELECT is_admin FROM role WHERE user_id = ?", (user_id,))
        is_admin = self.cur.fetchone()
        return is_admin[0] == 1

    def update_activity(self, capacity, start_time, end_time, title, status, description, department, cover, location,
                        registration_time, activity_id):
        self.cur.execute("UPDATE activities SET capacity = ?, startTime = ?, endTime = ?, title = ?, status = ?, description = ?, department = ?, cover = ?, location = ?, registration_time = ?, enrolled = enrolled WHERE id = ?", (capacity, start_time, end_time, title, status, description, department, cover, location, registration_time, activity_id))
        self.conn.commit()
        self.check_activity_status(activity_id)

    def update_password(self, user_id, new_password):
        new_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
        self.cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        self.conn.commit()

    def get_signup_data(self, activity_id):
        self.check_activity_status(activity_id)
        self.cur.execute("SELECT users.username, users.name, signup.created_at FROM users INNER JOIN signup ON users.id = signup.user_id WHERE signup.activity_id = ?", (activity_id,))
        signup_data = self.cur.fetchall()
        return signup_data

    def check_activity_status(self, activity_id) -> None:
        if type(activity_id) is tuple:
            activity_id = activity_id[0]
        self.cur.execute("SELECT status FROM activities WHERE id = ?", (activity_id,))
        status = self.cur.fetchone()
        if status is None:
            return
        else:
            self.cur.execute("SELECT startTime, endTime FROM activities WHERE id = ?", (activity_id,))
            times = self.cur.fetchall()
            start_time = datetime.strptime(times[0][0], '%Y-%m-%dT%H:%M:%S%z').timestamp()
            end_time = datetime.strptime(times[0][1], '%Y-%m-%dT%H:%M:%S%z').timestamp()
            now_time = time.time()
            if now_time < start_time:
                return
            elif start_time < now_time < end_time:
                self.cur.execute("UPDATE activities SET status = 'ongoing' WHERE id = ?", (activity_id,))
                self.conn.commit()
                return
            else:
                self.cur.execute("UPDATE activities SET status = 'ended' WHERE id = ?", (activity_id,))
                self.conn.commit()
                return
