from Database import Database

database = Database()
database.connect()
models = database.models
engine = database.engine
