from peewee import SqliteDatabase, Model, CharField, AutoField

database_tnts = SqliteDatabase('./databases/to-do-list.db')

class BaseModel(Model):
    class Meta:
        database = database_tnts

# TASKS TODAY
class TaskToday(BaseModel):
    id = AutoField(primary_key=True, unique=True)  # Auto-incrementing primary key, non-null, and unique
    task = CharField(null=False)

    class Meta:
        db_table = 'task_today'  # Set the table name

# TASKS NTS
class TaskNTS(BaseModel):
    id = AutoField(primary_key=True, unique=True)  # Auto-incrementing primary key, non-null, and unique
    task = CharField(null=False)

    class Meta:
        db_table = 'task_nts'  # Set the table name

# TASKS FOREVER
class TaskForever(BaseModel):
    id = AutoField(primary_key=True, unique=True)  # Auto-incrementing primary key, non-null, and unique
    task = CharField(null=False)

    class Meta:
        db_table = 'task_forever'  # Set the table name
