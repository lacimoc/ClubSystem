# 社团活动报名系统

这是一个宁德师范学院计算机协会的社团活动报名系统

后端采用Flask实现

前端采用Vue3实现

[前端项目ClubSystemWeb（暂未上传）](https://github.com/lacimoc/)

# 如何使用

如何使用该系统

### 初次使用

确保完成以下步骤

- 运行db_init.py初始化数据库

- 安装相应的第三方库

  ```bash
  pip install flask_cors
  pip install bcrypt
  pip install pandas
  ```

  

- 开放对应的端口（或使用Nginx反向代理）

### 如何启动程序

可以在以下两种方式中选择一种

- 使用WSGI服务器（推荐）

  1. 安装Gunicorn

     ```bash
     pip install gunicorn
     ```

     

  2. 启动Gunicorn服务器

     ``` bash
     gunicorn -w 4 app:app
     ```

     

- 使用Python Flask开发环境

  1. 更改 **app.py** 中的 **port** 参数
  2. 启动 **app.py**

# 计划完成的内容

- [x] token校验失败后返回401
- [x] 非admin用户在token检验失败后返回403而非200
- [ ] 用户账户数据导入
