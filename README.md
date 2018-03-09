# flask-bbs
---------------------
模仿cnode论坛用flask实现的一个论坛
---------------------
- 论坛实现了用户注册、登陆、上传头像、发表文章、评论、私信等功能
- 对用户密码使用SHA256并加盐处理
- 使用MongoDB存储数据并实现相应的ORM
- 利用jinja2模板实现网页模板，解耦页面与业务逻辑，提高代码重用度
- 使用Nginx反向代理，处理静态文件，同时配合gunicorn实现多进程的负载均衡
- 利用Python uuid模块生成随机数防范CSRF攻击
---------------------
论坛操作如下所示：
![image](https://github.com/wangqian6151/flask-bbs/blob/master/bbs.gif)
