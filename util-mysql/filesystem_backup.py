__author__ = 'zhenanye'
# coding=utf-8
from storage import get_storage
from util import get_uuid
from db import User, Group, Membership, File, Folder, Shared
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class FileSystem():

    def __init__(self, uid):
        # load storage driver
        self.storage = get_storage('mock', uid=uid)
        self.uid = uid

        engine = create_engine('sqlite:///C:\\Users\\xiang\\test.db')

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_file(self, folder_id, file_name):

        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()
        uuid = get_uuid(folder.path, file_name)

        child_files = self.read_folder(folder_id)['files']

        for i in child_files:
            if file_name == i['name']:
                return 'file already exists'

        file = File(folder_id=folder.id, name=file_name, user_id=self.uid, location=uuid, type='sheepdog', deleted=False)

        upload_result = self.storage.create_object(file=file_name, uuid=uuid)

        if upload_result:
            self.session.add(file)
            self.session.commit()
        else:
            self.session.rollback()

    def read_file(self, file_id):
        file = self.session.query(File).filter_by(id=file_id).first()
        return self.storage.get_object(uuid=file.location)

    def update_file(self, file_id, file_name):
        file = self.session.query(File).filter_by(id=file_id).first()
        if self.storage.update_object(file=file_name, uuid=file.location):
            return file.serialize

    def rename_file(self, file_id, new_name):
        file = self.session.query(File).filter_by(id=file_id).first()
        file.name = new_name

        self.session.commit()
        return file.serialize

    def move_file(self, old_folder_id, new_folder_id, file_id):
        file = self.session.query(File).filter_by(id=file_id).first()
        file.folder_id = new_folder_id

        self.session.commit()
        return file.serialize

    def delete_file(self, file_id):
        file = self.session.query(File).filter_by(id=file_id).first()
        file.deleted = True
        self.session.commit()

    def create_folder(self, parent_folder_id, name):

        parent_folder = self.session.query(Folder).filter_by(id=parent_folder_id, user_id=self.uid).first()

        child_folders = self.read_folder(parent_folder_id)['folders']

        for i in child_folders:
            if name == i['name']:
                print "Folder name already exists"
                return

        parent_folder_path = parent_folder.path
        if parent_folder.path == '/': parent_folder_path = ''
        folder = Folder(user_id=self.uid, parent_id=parent_folder.id, path=parent_folder_path+'/'+name, name=name, deleted=False)

        self.session.add(folder)
        self.session.commit()
        return folder.serialize

    def read_folder(self, folder_id):
        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()
        child_folders = []
        for i in self.session.query(Folder).filter_by(parent_id=folder_id, deleted=False).all():
            child_folders.append(i.serialize)
        child_files = []
        for i in self.session.query(File).filter_by(folder_id=folder.id, deleted=False).all():
            child_files.append(i.serialize)

        return {'folders': child_folders, 'files': child_files}

    def delete_folder(self, folder_id):
        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid).first()

        childs = self.read_folder(folder_id)
        for child_folder in childs['folders']:
            self.delete_folder(child_folder['id'])

        for child_file in childs['files']:
            self.delete_file(child_file['id'])

        folder.deleted = True
        self.session.commit()

    def rename_folder(self, folder_id, new_name):
        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid, deleted=False).first()

        new_path='/'.join(folder.pat.split('/')[:-1]) + new_name

        folder.path = new_path
        folder.name = new_name
        self.session.commit()
        return folder.serialize

    def move_folder(self, folder_id, new_parent_folder_id):
        folder = self.session.query(Folder).filter_by(id=folder_id)
        folder.parent_id = new_parent_folder_id

        self.session.commit()
        return folder.serialize

    def share_file(self, file_id, privilege, target_user='', target_group=''):
        file = self.session.query(File).filter_by(id=file_id, user_id=self.uid)

        if (target_group == '' and target_user == '') or (target_group != '' and target_user != ''):
            return False

        if target_group == '':
            target_group = None
        if target_user == '':
            target_user = None

        share_file = Shared(from_user_id=self.uid, to_user_id=target_user, to_group_id=target_group, folder_id=None,
                            file_id=file.id, privilege=privilege)

        self.session.add(share_file)
        self.session.commit()

    def share_folder(self, folder_id, privilege, target_user='', target_group=''):
        folder = self.session.query(Folder).filter_by(id=folder_id, user_id=self.uid)

        if (target_group == '' and target_user == '') or (target_group != '' and target_user != ''):
            raise Exception

        if target_group == '':
            target_group = None
        if target_user == '':
            target_user = None

        share_folder = Shared(from_user_id=self.uid, to_user_id=target_user, to_group_id=target_group, folder_id=folder_id, file_id=None, privilege=privilege)

        self.session.add(share_folder)
        self.session.commit()

    def read_sharedfolder(self, path):
        pass

    def delete_shared_file(self):
        pass