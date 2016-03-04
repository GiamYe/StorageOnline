__author__ = 'zhenanye'
# coding = utf8

from flask import Flask, request, session, url_for, redirect, jsonify, abort, g
#from flask.ext.httpauth import HTTPBasicAuth
import filesystem
from db import db_session
from model import User, Group, Membership, Folder
from functools import wraps

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_POOL_SIZE = 10,
    SQLALCHEMY_ECHO = True
)
#auth = HTTPBasicAuth()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#@auth.verify_password
def verify_password(username_or_token, password=''):
    if username_or_token=='':
        return False
    #import pdb;pdb.set_trace()
    user = User.verify_token(username_or_token)
    if user is None:
        user = db_session.query(User).filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

#@app.route('/token')
#@auth.login_required
def get_token():
    token = g.user.generate_token(600)
    return jsonify({'user_id':g.user.id, 'username':g.user.name, 'token': token.decode('ascii'), 'duration': 600})

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #import pdb;pdb.set_trace()
        if 'X-Token' not in request.headers:
            abort(401)
        if not verify_password(request.headers.get('X-Token')):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

@app.route('/register', methods=['POST'])
def register():
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        user_json = request.get_json(force=True)
        username = user_json.get('username')
        password = user_json.get('password')
        email = user_json.get('email')
        if username is None or password is None:
            abort(400)
        if db_session.query(User).filter_by(name=username).first() is not None:
            abort(400)
        user = User(name=username, password=password, email=email)
        db_session.add(user)
        db_session.commit()
        root_folder= Folder(user_id=user.id, path="/", name="/", deleted=False)
        shared_folder= Folder(user_id=user.id, path="/shared", name="shared", deleted=False)
        trash_folder= Folder(user_id=user.id, path="/trash", name="trash", deleted=False)
        db_session.add(root_folder)
        db_session.add(shared_folder)
        db_session.add(trash_folder)
        db_session.commit()
        return jsonify({'username':user.name})

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        user_pwd = request.get_json(force=True)
        username = user_pwd['username']
        password = user_pwd['password']
        if not verify_password(username, password):
            abort(401)
        return get_token()

@app.route('/users', methods=['GET'])
@login_required
def users():
    if request.method == 'GET':
        user_list = []
        for i in db_session.query(User).all():
            groups=[]
            for j in db_session.query(Membership).filter_by(user_id=i.id).all():
                groups.append(db_session.query(Group).filter_by(id=j.group_id).first().name)
            user_info = i.serialize
            user_info['groups'] = groups
            user_list.append(user_info)
        return jsonify({'users': user_list})

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def user_by_id(user_id):
    if request.method == 'DELETE':
        user =db_session.query(User).filter_by(id=user_id).first()
        db_session.delete(user)
        # for i in db_session.query(Membership).filter_by(user_id=user_id).all():
        #     db_session.delete(i)
        db_session.commit()
        return ""

@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    if request.method == 'GET':
        groups = []
        for i in db_session.query(Group).all():
            users=[]
            for j in db_session.query(Membership).filter_by(group_id=i.id).all():
                users.append(db_session.query(User).filter_by(id=j.user_id).first().name)
            group_info = i.serialize
            group_info['users'] = users
            groups.append(group_info)
        return jsonify({'groups': groups})
    if request.method == 'POST':
        group = request.get_json(force=True)
        new_group = Group(name=group['name'])
        db_session.add(new_group)
        db_session.commit()
        return jsonify(new_group.serialize)

@app.route('/group/<int:group_id>', methods=['GET', 'DELETE'])
#@login_required
def group_by_id(group_id):
    if request.method == 'GET':
        group = db_session.query(Group).filter_by(id=group_id).first()
        group_info = group.serialize
        users = []
        for i in db_session.query(Membership).filter_by(group_id=group_id).all():
            users.append(db_session.query(User).filter_by(id=i.user_id).first().serialize)
        group_info['users']=users;
        return jsonify({'group':group_info})
         

    if request.method == 'DELETE':
        group =db_session.query(Group).filter_by(id=group_id).first()
        db_session.delete(group)
        # for i in db_session.query(Membership).filter_by(group_id=group_id).all():
        #     db_session.delete(i)
        db_session.commit()
        return ""

@app.route('/membership', methods=['POST'])
@login_required
def membership():
    if request.method == 'POST':
        ms = request.get_json(force=True)
        new_ms = Membership(user_id=ms['user_id'], group_id=ms['group_id'])
        db_session.add(new_ms)
        db_session.commit()
        return jsonify(new_ms.serialize)

@app.route('/folder', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def root_folder():
    #user = request.args.get('user')
    #import pdb;pdb.set_trace()
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'GET':
        return jsonify(fs.read_folder('/'))
    elif request.method == 'POST':
        #create folder
        folder = request.get_json(force=True)
        print 'create folder'
        print folder
        return jsonify(fs.create_folder(folder))
    elif request.method == 'PUT':
        folder = request.get_json(force=True)
        return jsonify(fs.update_folder(folder))
    elif request.method == 'DELETE':
        folder = request.get_json(force=True)
        return jsonify(fs.recycle_folder('/'))

@app.route('/folder/<path:folder_path>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def folder(folder_path):
    #import pdb;pdb.set_trace()
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    folder_path = '/'+folder_path
    if request.method == 'GET':
        return jsonify(fs.read_folder(folder_path))
    elif request.method == 'PUT':
        folder = request.get_json(force=True)
        print folder
        return jsonify(fs.update_folder(folder, folder_path))
    
@app.route('/folder/<int:folder_id>', methods=['DELETE'])
@login_required
def folder_by_id(folder_id):
    #import pdb;pdb.set_trace()
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'DELETE':
        return jsonify(fs.recycle_folder(folder_id))

@app.route('/file', methods=['POST'])
@login_required
def create_file():
    #user = request.args.get('user')
    #import pdb;pdb.set_trace()
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'POST':
        #create folder
        file = request.get_json(force=True)
        print file
        return jsonify(fs.create_file(file))

@app.route('/file/<int:file_id>',methods=['GET', 'PUT', 'DELETE'])
@login_required
def file_by_id(file_id):
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'GET':
        return jsonify(fs.read_file_by_id(file_id))
    elif request.method == 'PUT':
        file = request.get_json(force=True)
        return jsonify(fs.update_file(file, '/', file_id))
    elif request.method == 'DELETE':
        return jsonify(fs.recycle_file(file_id))

@app.route('/file/<path:folder_path>/<file_name>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def file(folder_path, file_name):
    #user = request.args.get('user')
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    folder_path = '/'+folder_path
    if request.method == 'GET':
        return jsonify(fs.read_file(folder_path, file_name)).encode("ISO-8859-1")
    elif request.method == 'PUT':
        file = request.get_json(force=True)
        return jsonify(fs.update_file(file, folder_path, file_name))
    elif request.method == 'DELETE':
        return jsonify(fs.delete_file(folder_path, file_name))

@app.route('/shared/folder', methods=['POST'])
@login_required
def share_folder():
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        share_item = request.get_json(force=True)
        return jsonify(fs.share_folder(share_item['to_user'], share_item['folder_id']))
    else:
        return 'access denied'

@app.route('/shared/file', methods=['POST'])
@login_required
def share_file():
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'POST':
        share_item = request.get_json(force=True)
        return jsonify(fs.share_file(share_item['to_user'], share_item['file_id']))
    else:
        return 'access denied'

@app.route('/trash/folder/<int:folder_id>', methods=['DELETE'])
@login_required
def trash_folder(folder_id):
    #import pdb;pdb.set_trace()
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'DELETE':
        return jsonify(fs.delete_folder_by_id(folder_id))

@app.route('/trash/file/<int:file_id>', methods=['DELETE'])
@login_required
def trash_file(file_id):
    user = g.user.id
    fs = filesystem.FileSystem(user, db_session)
    if request.method == 'DELETE':
        return jsonify(fs.delete_file_by_id(file_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
