from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename
from models.user import User
from models.topic import Topic
import os
import uuid

from routes import current_user,new_csrf_token
from utils import log

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login u', u)
    if u is None:
        # 转到 topic.index 页面
        # return redirect(url_for('topic.index'))
        return redirect(url_for('index.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login', session)
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        # abort(404)
        return redirect(url_for('.index'))
    else:
        board_id = int(request.args.get('board_id', -1))
        recent_topics = Topic.recent_topic(u.id)
        recent_replies = Topic.recent_reply(u.id)
        return render_template('profile.html', user=u, bid=board_id,
                               recent_topics=recent_topics, recent_replies=recent_replies)


@main.route('/user/<string:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        # abort(404)
        return redirect(url_for('.index'))
    else:
        board_id = int(request.args.get('board_id', -1))
        recent_topics = Topic.recent_topic(id)
        recent_replies = Topic.recent_reply(id)
        return render_template('profile.html', user=u, bid=board_id,
                               recent_topics=recent_topics, recent_replies=recent_replies)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    # file 是一个上传的文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        # filename = secure_filename(file.filename)
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u = current_user()
        User.update(u.id, dict(
            user_image='/uploads/{}'.format(filename)
        ))

    return redirect(url_for(".profile"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    token = new_csrf_token()
    return render_template('setting.html', user=u, token=token)


@main.route('/setting/save', methods=["POST"])
def save_setting():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    form = request.form
    User.update(u.id, form)
    return redirect(url_for(".profile"))


@main.route('/password/save', methods=['POST'])
def save_password():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    form = request.form
    if User.salted_password(form['old_pass']) == u.password:
        new_pass = User.salted_password(str(form.get('new_pass')))
        u.password = new_pass
        u.save()
        return redirect(url_for('.profile'))
    return redirect(url_for('.setting'))


@main.route('/signout', methods=["POST", "GET"])
def signout():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    session.pop("user_id")
    return redirect(url_for('.index'))

