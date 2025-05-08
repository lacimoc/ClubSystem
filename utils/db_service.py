import time
from datetime import datetime
import sqlite3
import bcrypt


class DBService(object):
    def __init__(self) -> None:
        """
        实例化连接数据库
        """
        self.conn = sqlite3.connect('./db/database.db')
        self.cur = self.conn.cursor()

    # 初始化数据库，创建表，没有表则创建
    def init_db(self) -> None:
        """
        初始化数据库，创建表，没有表则创建
        :return: None
        """
        # 创建users表
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        # 创建role表
        self.cur.execute('''CREATE TABLE IF NOT EXISTS role (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL,
                            is_admin BOOLEAN NOT NULL
                        )''')
        # 创建groups表
        self.cur.execute('''CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_id INTEGER NOT NULL,
                            group_name TEXT NOT NULL
                        )''')
        # 创建activities表
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
        # 创建signup表
        self.cur.execute('''CREATE TABLE IF NOT EXISTS signup (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            activity_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        self.conn.commit()

    def add_user(self, username: str, password: str, name: str) -> None:
        """
        数据库添加用户
        :param username: 用户名
        :param password: 密码
        :param name: 姓名
        :return: None
        """
        is_insert = self.conn.execute("SELECT * FROM users WHERE username =?", (username,)).fetchone()
        if is_insert is None:
            hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            self.conn.execute("INSERT INTO users (username, password, name) VALUES (?,?,?)", (username, hashed_password, name))
            self.conn.commit()

    def get_password(self, username: str) -> str | None:
        """
        数据库获取用户密码
        :param username: 用户名
        :return: 获取到的密码或None
        """
        self.cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        db_pwd = self.cur.fetchone()
        if db_pwd:
            return db_pwd[0]
        else:
            return None

    def get_user_id(self, username: str) -> int | None:
        """
        数据库获取用户id
        :param username: 用户名
        :return: 获取到的id或None
        """
        self.cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        db_id = self.cur.fetchone()
        if db_id:
            return db_id[0]
        else:
            return None

    def get_all_users(self) -> list[tuple]:
        """
        数据库获取所有用户信息
        :return: 含有所有用户信息的列表
        """
        # 联合查询users和role和groups表，获取所有用户信息
        self.cur.execute("SELECT users.id, users.username, users.created_at, groups.id, role.is_admin, users.name FROM users INNER JOIN role ON users.id = role.user_id INNER JOIN groups ON role.group_id = groups.id ORDER BY role.group_id, role.is_admin DESC")
        users = self.cur.fetchall()
        return users

    def create_user(self, department: int, username: str, password: str, name: str, is_admin: bool = False) -> None:
        """
        数据库创建用户
        :param department: 部门id
        :param username: 用户名
        :param password: 密码
        :param name: 姓名
        :param is_admin: 是否为管理员
        :return: None
        """
        self.add_user(username, password, name)
        user_id = self.get_user_id(username)
        self.cur.execute("INSERT INTO role (user_id, group_id, is_admin) VALUES (?,?,?)", (user_id, department, is_admin))
        self.conn.commit()

    def delete_user(self, user_id: int) -> None:
        """
        数据库删除用户
        :param user_id: 用户id
        :return: None
        """
        self.cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.cur.execute("DELETE FROM role WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def reset_password(self, user_id: int) -> None:
        """
        数据库重置密码为123456
        :param user_id: 用户id
        :return: None
        """
        password = bcrypt.hashpw(b"123456", bcrypt.gensalt())
        self.cur.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))
        self.conn.commit()

    def create_activity(self, capacity: int, enrolled: int, start_time, end_time, title: str, status: str, description: str, department: str, cover: str,
                        location: str, registration_time) -> None:
        self.cur.execute("INSERT INTO activities (capacity, enrolled, startTime, endTime, title, status, description, department, cover, location, registration_time) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (capacity, enrolled, start_time, end_time, title, status, description, department, cover, location, registration_time))
        self.conn.commit()

    def get_user_info(self, user_id: int) -> tuple | None:
        """
        数据库获取用户信息
        :param user_id: 用户id
        :return: 返回用户信息或None
        """
        self.cur.execute("SELECT users.username, role.is_admin FROM users INNER JOIN role ON users.id = role.user_id WHERE users.id = ?", (user_id,))
        user_info = self.cur.fetchone()
        return user_info

    def enroll_activity(self, active_id: int, user_id: int) -> None:
        """
        数据库报名活动
        :param active_id: 活动id
        :param user_id: 用户id
        :return: None
        """
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

    def get_activities(self, user_id: int) -> tuple[list[tuple], str]:
        """
        数据库获取用户报名的活动信息
        :param user_id: 用户id
        :return: 活动信息列表和部门名称
        """
        activity_ids = self.cur.execute("SELECT id FROM activities").fetchall()
        for i in activity_ids:
            self.check_activity_status(i)
        department = self.cur.execute("SELECT group_id FROM role WHERE user_id = ?", (user_id,)).fetchone()
        if department is None:
            return [tuple()], ''
        department_text = self.cur.execute("SELECT group_name FROM groups WHERE id = ?", (department[0],)).fetchone()
        self.cur.execute("SELECT activities.id, activities.title, activities.status, activities.startTime, activities.endTime, activities.description, activities.department, activities.cover, activities.location , activities.enrolled, activities.capacity, activities.registration_time FROM activities")
        activities = self.cur.fetchall()
        return activities, department_text

    def get_user_activity_info(self, user_id: int) -> list[tuple]:
        """
        数据库获取用户报名的活动信息
        :param user_id: 用户id
        :return: 用户报名的活动信息列表
        """
        all_signed_activity_ids = self.cur.execute("SELECT activity_id FROM signup WHERE user_id = ?", (user_id,)).fetchone()
        if all_signed_activity_ids is None:
            return []
        for i in all_signed_activity_ids:
            self.check_activity_status(i)
        self.cur.execute("SELECT activities.id, activities.title, activities.status, activities.startTime, activities.endTime, activities.description, activities.department, activities.cover, activities.location , activities.enrolled, activities.capacity FROM activities WHERE id IN ({})".format(','.join('?' * len(all_signed_activity_ids))), all_signed_activity_ids)
        activities = self.cur.fetchall()
        return activities

    def cancel_enroll_activity(self, active_id: int, user_id: int) -> None:
        """
        数据库取消报名活动
        :param active_id: 活动id
        :param user_id: 用户id
        :return: None
        """
        self.check_activity_status(active_id)
        self.cur.execute("DELETE FROM signup WHERE user_id = ? AND activity_id = ?", (user_id, active_id))
        self.cur.execute("UPDATE activities SET enrolled = enrolled - 1 WHERE id = ?", (active_id,))
        self.conn.commit()

    def delete_activity(self, activity_id: int) -> None:
        """
        数据库删除活动
        :param activity_id: 活动id
        :return: None
        """
        self.cur.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        self.cur.execute("DELETE FROM signup WHERE activity_id = ?", (activity_id,))
        self.conn.commit()

    def is_admin(self, user_id: int) -> bool:
        """
        数据库判断用户是否为管理员
        :param user_id: 用户id
        :return: 是否为管理员
        """
        self.cur.execute("SELECT is_admin FROM role WHERE user_id = ?", (user_id,))
        is_admin = self.cur.fetchone()
        return is_admin[0] == 1

    def update_activity(self, capacity, start_time, end_time, title, status, description, department, cover, location,
                        registration_time, activity_id):
        self.cur.execute("UPDATE activities SET capacity = ?, startTime = ?, endTime = ?, title = ?, status = ?, description = ?, department = ?, cover = ?, location = ?, registration_time = ?, enrolled = enrolled WHERE id = ?", (capacity, start_time, end_time, title, status, description, department, cover, location, registration_time, activity_id))
        self.conn.commit()
        self.check_activity_status(activity_id)

    def update_password(self, user_id: int, new_password: str) -> None:
        """
        数据库更新密码
        :param user_id: 用户id
        :param new_password: 新密码
        :return: None
        """
        new_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
        self.cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        self.conn.commit()

    def get_signup_data(self, activity_id: int) -> list[tuple]:
        """
        数据库获取报名数据
        :param activity_id: 活动id
        :return: 活动报名数据列表
        """
        self.check_activity_status(activity_id)
        self.cur.execute("SELECT users.username, users.name, signup.created_at FROM users INNER JOIN signup ON users.id = signup.user_id WHERE signup.activity_id = ?", (activity_id,))
        signup_data = self.cur.fetchall()
        return signup_data

    def check_activity_status(self, activity_id: int | tuple) -> None:
        """
        检查活动状态，并更新数据库
        :param activity_id: 活动id
        :return: None
        """
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
