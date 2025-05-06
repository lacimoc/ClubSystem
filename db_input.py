from utils import db_service
import pandas as pd


department_dict = {
    "技术部": 1,
    "办公室部": 2,
    "策划部": 3,
    "财务部": 4,
    "电竞部": 5,
    "社务部": 6,
    "宣传部": 7
}


if __name__ == '__main__':
    db = db_service.DBService()
    data = pd.read_excel('data.xlsx')
    rows_list = []

    for index, row in data.iterrows():
        rows_list.append(row.tolist())

    for row in rows_list:
        db.create_user(department_dict.get(row[3], 1), str(row[1]), str(row[1]), row[2], int(row[5]) == 1)
