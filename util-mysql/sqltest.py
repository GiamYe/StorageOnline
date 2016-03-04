__author__ = 'zhenanye'

from db import User, Group, Membership, File, Folder, Shared
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://ypan:ypan@172.16.17.201:3306/ypan', echo=True)
session = sessionmaker(bind=engine)()

f = session.query(Folder).filter_by(path='/').first()

print f.id

u = session.query(User).filter_by(id=5).first()

print u.id
