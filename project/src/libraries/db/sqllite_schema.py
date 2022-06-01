import sqlalchemy
import project.src.libraries.db.model as model

sqlite_engine = sqlalchemy.create_engine('sqlite:///:memory')

metadata_obj = sqlalchemy.MetaData()

model.getKey(metadata_obj)

metadata_obj.create_all(sqlite_engine)

