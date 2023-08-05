# sql_operation

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Sachin Indoriya (c) 2022

## Examples of How To Use (Buggy Alpha Version)


```python 
from sql_operations  import SqlDB

 
# mysql connection credentials
USERNAME = 'username'
PASSWORD = 'password'
DATABASE = 'database_name'
HOST = 'host'

# create SqlDB object
sql_db = SqlDB(dummy_data)

# check sql server is connected or not
if sql_db.is_conneted():
    print("Hurrey!!!, sql server connected.")
else:
    print("sql server not connected.")


# create a table
table_name = "new_table"
columns = ['col_1','col_2','col_3']
sql_db.create_table(table_name,columns)


# check table created or not
if sql_db.check_table_exist():
    print("table exist")
else:
    print("table not exist")

# insert row into table
table_name = "new_table"
row = ['val_1','val_2','val_3']
if sql_db.insert_into_table() == 1:
    print("row inserted")
    

# read row from the table
table_name = "new_table"
item_id = "item_id"
rows = sql_db.read_rows(table_name,item_id)
print(rows)

# delete row from table
table_name = "new_table"
item_id = "item_id"
if sql_db.delete_rows(table_name,item_id) == 1:
    print("row deleted")

# close database connection
sql_db.close_conn()
```


 
