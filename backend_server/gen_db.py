from sqlalchemy import create_engine, MetaData,Table, Column, Integer, String, ForeignKey, Text,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
from courseCSVImporter import *
from newsCSVImporter import *
from postImporter import *

# creat database
db.metadata.create_all(db.engine)
DBSession = sessionmaker(bind=db.engine)
session = DBSession()
newsImporter()
courseImporter()
postImporter()
session.commit()
session.close()