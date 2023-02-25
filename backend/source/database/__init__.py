from source.database.Database import Database

database = Database()
database.drop_data()
database.connect()
models = database.models
engine = database.engine
