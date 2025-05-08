import uuid

from utils import db_service
import pandas as pd


def export(activity_id: int) -> str:
    """
    从数据库中导出报名表为Excel文件
    :param activity_id: 活动ID
    :return: 文件位置
    """
    db = db_service.DBService()
    signup_data = db.get_signup_data(int(activity_id))
    if signup_data is None:
        return ''
    else:
        pandas_df = pd.DataFrame(signup_data, columns=['学号', '姓名', '报名时间'])
        filename = str(uuid.uuid4()) + '.xlsx'
        pandas_df.to_excel(f'static/form/{filename}', index=False)
        return filename

