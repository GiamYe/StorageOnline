__author__ = 'zhenanye'
# coding=utf-8
from storage import get_storage
from util import get_uuid
from model import User, Group, Membership, File, Folder, Shared
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime


class FileSystem():

    def __init__(self, uid, session):
        # load storage driver
        self.storage_type = 'awss3'
        self.storage = get_storage(self.storage_type)
        self.uid = uid

        self.session = session

    def validate_file(self, file, folder_path='', file_name='', action=''):

        validate_pass = True
        if action == 'create':
            folder_id = file.get('folder_id')
            name = file.get('name')
            folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()
            if folder == None:
                return False
            child_files = self.read_folder(folder.path)['files']
            for child_file in child_files:
                if name == child_file['name']:
                    return False

        if action == 'update':
            folder_id = file.get('folder_id')
            name = file.get('name')
            folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()
            if folder == None:
                return False
            child_files = self.read_folder(folder.path)['files']
            for child_file in child_files:
                if name == child_file['name']:
                    return False
        return True

    def validate_folder(self, folder, folder_path='', action=''):

        if action == 'update':
            parent_id = folder.get('parent_id')
            name = folder.get('name')
            path = folder.get('path')

            parent_folder = self.session.query(Folder).filter_by(id=parent_id).first()
            if parent_folder is None:
                return False

            if parent_folder.path == '/':
                if '/'+name != path:
                    return False
            elif parent_folder.path+'/'+name != path:
                return False
            child_folders = self.read_folder(parent_folder.path)['folders']
            for child_folder in child_folders:
                if name == child_folder['name']:
                    print "Folder name already exists"
                    return False

        if action == 'create':
            parent_id = folder.get('parent_id')
            name = folder.get('name')
            path = folder.get('path')
            parent_folder = self.session.query(Folder).filter_by(id=parent_id).first()
            if parent_folder.path == '/':
                if '/'+name != path:
                    return False
            elif parent_folder.path+'/'+name != path:
                return False
            child_folders = self.read_folder(parent_folder.path)['folders']
            for child_folder in child_folders:
                if name == child_folder['name']:
                    print "Folder name already exists"
                    return False
        return True

    def create_file(self, file):

        if self.validate_file(file, action='create') == False:
            raise IOError('validation failed')
        folder = self.session.query(Folder).filter_by(id=file.get('folder_id'), user_id=self.uid).first()
        uuid = get_uuid(str(self.uid), folder.path, file['name'])
        #content = unicode(file.get('content'), "ISO-8859-1")
        content = file.get('content').encode("ISO-8859-1")
        child_files = self.read_folder(folder.path)['files']

        for i in child_files:
            if file['name'] == i['name']:
                return 'file already exists'

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_rec = File(folder_id=folder.id, name=file['name'], user_id=self.uid, location=uuid,
                        type=self.storage_type, deleted=False, ctime=now)

        try:
            upload_result = self.storage.create_object(content=content, uuid=uuid)
            if upload_result:
                self.session.add(file_rec)
                self.session.commit()
                return file_rec.serialize
            else:
                self.session.rollback()
        except IOError:
            self.session.rollback()


    def read_file(self, folder_path, file_name):

        folder = self.session.query(Folder).filter_by(path=folder_path, user_id=self.uid).first()
        file = self.session.query(File).filter_by(folder_id=folder.id, user_id=self.uid, name=file_name).first()
        json_file = file.serialize

        try:
            json_file['content'] = self.storage.get_object(uuid=file.location)
        except IOError:
            raise IOError('failed to read file')

        return json_file

    def read_file_by_id(self, file_id):
        file = self.session.query(File).filter_by(id=file_id, deleted=False).first()
        json_file = file.serialize

        try:
            json_file['content'] = unicode(self.storage.get_object(uuid=file.location), "ISO-8859-1")
        except IOError:
            raise IOError('failed to read file')

        return json_file

    def update_file(self, file, folder_path, file_name):
        if self.validate_file(file, folder_path, action='update') == False:
            raise IOError('validation failed')
        file_rec = self.session.query(File).filter_by(id=file['id']).first()
        file_rec.name = file['name']
        file_rec.folder_id = file['folder_id']
        content = file.get('content')

        if content:
            try:
                self.storage.update_object(content=content, uuid=file.location)
            except IOError:
                raise IOError('failed to update file')

        self.session.commit()
        return file_rec.serialize

    def delete_file(self, folder_path, file_name):
        folder = self.session.query(Folder).filter_by(path=folder_path, user_id=self.uid).first()
        file = self.session.query(File).filter_by(folder_id=folder.id, user_id=self.uid, name=file_name).first()
        file.deleted = True
        self.session.commit()
        return ""

    def delete_file_by_id(self, file_id):
        file = self.session.query(File).filter_by(id=file_id).first()
        #file.deleted = True
        self.session.delete(file)
        self.session.commit()
        return ""

    def create_folder(self, folder):

        if self.validate_folder(folder, action='create') == False:
            raise IOError('validation failed')
        parent_id = folder['parent_id']
        folder_name = folder['name']
        folder_path = folder['path']

        parent_folder = self.session.query(Folder).filter_by(id=parent_id, user_id=self.uid).first()

        child_folders = self.read_folder(parent_folder.path)['folders']

        for i in child_folders:
            if folder_name == i['name']:
                print "Folder name already exists"
                return
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        folder_rec = Folder(user_id=self.uid, parent_id=parent_folder.id, path=folder_path, name=folder_name, deleted=False, ctime=now)

        self.session.add(folder_rec)
        self.session.commit()
        return folder_rec.serialize

    def read_folder(self, folder_path):
        #import pdb;pdb.set_trace()
        folder = self.session.query(Folder).filter_by(path=folder_path, user_id=self.uid, deleted=False).first()
        child_folders = []
        for i in self.session.query(Folder).filter_by(parent_id=folder.id, deleted=False).all():
            child_folders.append(i.serialize)
        child_files = []
        for i in self.session.query(File).filter_by(folder_id=folder.id, deleted=False).all():
            child_files.append(i.serialize)

        return {'folders': child_folders, 'files': child_files, 'folder':folder.serialize}

    #for shared and myshare
    def read_folder_by_id(self, folder_id):
        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()
        child_folders = []
        for i in self.session.query(Folder).filter_by(parent_id=folder.id).all():
            child_folders.append(i.serialize)
        child_files = []
        for i in self.session.query(File).filter_by(folder_id=folder.id).all():
            child_files.append(i.serialize)

        return {'folders': child_folders, 'files': child_files, 'folder':folder.serialize}

    def delete_folder_by_id(self, folder_id):
        #import pdb;pdb.set_trace()
        folder = self.session.query(Folder).filter_by(id=folder_id).first()

        for i in self.session.query(Folder).filter_by(parent_id=folder.id).all():
            self.delete_folder_by_id(i.id)

        # for child_file in self.session.query(File).filter_by(folder_id=folder_id):
        #     self.delete_file_by_id(child_file.id)

        #folder.deleted = True
        self.session.delete(folder)
        self.session.commit()
        return ""

    def update_folder(self, folder, folder_path):

        if self.validate_folder(folder, action='create') == False:
            raise IOError('validation failed')

        folder_rec = self.session.query(Folder).filter_by(id=folder.get('id'), user_id=self.uid, deleted=False).first()
        folder_rec.path = folder.get('path')
        folder_rec.name = folder.get('name')
        folder_rec.parent_id = folder.get('parent_id')

        self.session.commit()
        return folder_rec.serialize

    def rename_folder(self, folder_path, new_name):
        folder = self.session.query(Folder).filter_by(path=folder_path, user_id=self.uid, deleted=False).first()

        new_path='/'.join(folder.path.split('/')[:-1]) + new_name

        folder.path = new_path
        folder.name = new_name
        self.session.commit()
        return folder.serialize

    def move_folder(self, folder, parent):
        #folder = self.session.query(Folder).filter_by(path=folder_path, user_id=self.uid).first()
        #parent_path = '/'.join(new_path.split('/')[:-1])
        #parent_folder = self.session.query(Folder).filter_by(path=parent_path, user_id=self.uid).first()
        new_path = parent.path+'/'+folder.name
        folder.parent_id = parent.id
        folder.path = new_path
        for i in self.session.query(Folder).filter_by(parent_id=folder.id).all():
            self.move_folder(i,folder)

        self.session.commit()
        return 

    def copy_folder(self, to_user, parent_id, folder_name, folder_path):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_folder = Folder(user_id=to_user, parent_id=parent_id, name=folder_name, path=folder_path, deleted=False, ctime=now)
        self.session.add(new_folder)
        self.session.commit()
        return new_folder.serialize

    def copy_file(self, to_user,folder_id, file_name, file_location, type):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_file = File(user_id=to_user, folder_id=folder_id, name=file_name, location=file_location, type=type, deleted=False, ctime=now)
        self.session.add(new_file)
        self.session.commit()
        return 

    def copy(self, to_user, parent_id, parent_path, folder_name, folder_id):
        #import pdb;pdb.set_trace()
        newfolder = self.copy_folder(to_user, parent_id, folder_name, parent_path+'/'+folder_name)
        child_folders = self.session.query(Folder).filter_by(parent_id=folder_id).all()
        for i in child_folders:
            self.copy(to_user, newfolder['id'], newfolder['path'], i.name, i.id)
        for j in self.session.query(File).filter_by(folder_id=folder_id).all():
            self.copy_file(to_user, newfolder['id'], j.name, j.location, j.type)
        return

    def share_folder(self, to_user, folder_id):
        user_shared =self.session.query(Folder).filter_by(user_id=to_user, path='/shared').first()
        folder = self.session.query(Folder).filter_by(id=folder_id).first()
        self.copy(to_user, user_shared.id, user_shared.path, folder.name, folder_id)
        return ""

    def share_file(self, to_user, file_id):
        user_shared =self.session.query(Folder).filter_by(user_id=to_user, path='/shared').first()
        file = self.session.query(File).filter_by(id=file_id).first()
        self.copy_file(to_user, user_shared.id, file.name, file.location, file.type)
        return ""

    def recycle_folder(self, folder_id):
        folder = self.session.query(Folder).filter_by(id=folder_id).first()
        trash = self.session.query(Folder).filter_by(path='/trash', user_id=self.uid).first()
        self.move_folder(folder, trash)
        #folder.parent_id = trash.id
        #self.session.commit()
        #self.delete_folder(folder.path)
        return trash.serialize

    def recycle_file(self, file_id):
        #import pdb;pdb.set_trace()
        file = self.session.query(File).filter_by(id=file_id).first()
        trash = self.session.query(Folder).filter_by(path='/Trash', user_id=self.uid).first()
        file.folder_id = trash.id
        self.session.commit()
        #self.delete_file_by_id(file_id)
        return trash.serialize





