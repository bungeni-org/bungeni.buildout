"""
some database value population scripts
"""
from zope import component
from zope.configuration import xmlconfig
from bungeni.alchemist import Session
from bungeni.alchemist import security
from bungeni.alchemist.interfaces import IDatabaseEngine
from bungeni import models
from bungeni.models import schema
from bungeni_custom import sys
# load the workflows--adjusts the model with features as per each workflow
from bungeni.core.workflows import adapters

#from marginalia import schema as marginalia_schema
from sqlalchemy import create_engine

context = xmlconfig.file("db.zcml", package=sys)
schema.metadata.bind = db = component.getUtility(IDatabaseEngine, "bungeni-db")

schema.metadata.drop_all()
schema.metadata.create_all()

# load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
from alembic.config import Config
from alembic import command
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")

#schema.translation_lookup_index.create(db)

security.metadata.bind = db
security.metadata.drop_all() 
security.metadata.create_all() 

#marginalia_schema.metadata.bind = db
#marginalia_schema.metadata.drop_all()
#marginalia_schema.metadata.create_all() 

db.dispose()

