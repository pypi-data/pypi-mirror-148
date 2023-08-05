import logging
import time

import mysql.connector as mySql_connector
from mysql.connector import errorcode

from helpers import csv_to_list


class SqlDB:
    """
    SqlDB class is responsible for creating connection,manipulating and updating data on MySql database.
    """

    def __init__(self, username, password, host, database):
        self._conn = None
        """
        connect to mysql server and save the connection object.
        """
        try:
            self._conn = mySql_connector.connect(user=username, password=password, host=host, database=database)
            logging.info('connected to mysql server')
        except mySql_connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error(f"wrong username or password, Error: {repr(err)}")
            else:
                logging.error(f"can't connect to MySql, Error: {repr(err)}")

    def insert_from_csv(self, csv_file):
        """
        create a new table from csv file name and insert all csv file data to it.
        :param csv_file: binary file
        """

        # convert csv binary file data to list of tuples
        csv_data = csv_to_list(csv_file)

        if csv_data == -1:
            return -1
        else:
            table_name = csv_file.filename.replace('.csv', '')
            columns = csv_data[0]
            rows = csv_data[1:]

            # Check 'id' column in csv file exist or not
            if 'id' not in columns:
                logging.error(f'{csv_file} file does not contain "id" column')
                return -1

            if self.check_table_exist(table_name):
                cur_date = time.strftime('%Y_%m_%d_%H_%S')
                table_name = "%s_%s" % (table_name, str(cur_date))
                print(table_name)

            if self.create_table(table_name, columns) == 1:
                try:
                    self.insert_into_table(table_name, rows)
                    logging.debug(f'rows inserted into {table_name} table')
                except mySql_connector.errors.OperationalError as err:
                    logging.error(f"can't insert into {table_name} table, Error: {err}")
                    return -1
            else:
                return -1
        return 1

    def check_table_exist(self, table_name):
        if table_name == "":
            return False

        query = f"SHOW TABLES LIKE '%s'" % table_name
        db_cur = self._conn.cursor()
        db_cur.execute(query)
        result = db_cur.fetchone()

        if result is None:
            return False
        else:
            return True

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE {table_name} ( id varchar(100) PRIMARY KEY," + " varchar(100),".join(
            columns) + " varchar(100) )"
        cur = self._conn.cursor()
        try:
            cur.execute(query)
            logging.debug(f'{table_name} table created successfully')
            return 1
        except mySql_connector.Error as err:
            logging.error(f'sql query get failed {query}, Error: {repr(err)}')
            return -1

    def insert_into_table(self, table_name, rows):
        value_places = ["%s" for i in range(len(rows[0]))]
        query = f"INSERT INTO {table_name} VALUES (" + ",".join(value_places) + ")"

        cur = self._conn.cursor()

        try:
            cur.executemany(query, rows)
            self._conn.commit()
            logging.debug(f'inserted rows into {table_name}')
            return 1
        except mySql_connector.Error as err:
            logging.error(f'sql query get failed {query}, Error: {repr(err)}')
            return -1

    def read_rows(self, table_name, item_id=None):
        query = f"SELECT * FROM {table_name} "

        if item_id is not None:
            query += f"WHERE id='%s'" % item_id

        cur = self._conn.cursor()

        try:
            cur.execute(query)
            row_headers = [x[0] for x in cur.description]
            row_data = cur.fetchall()
            json_data = []
            for result in row_data:
                json_data.append(dict(zip(row_headers, result)))
            return json_data
        except mySql_connector.Error as err:
            logging.error(f'query failed {query}, Error: {repr(err)}')
            return -1

    def delete_row(self, table_name, item_id):
        """
        delete_row(), delete the rows from given table.
        """
        condition = "id='%s'" % item_id
        query = f"DELETE FROM {table_name} WHERE {condition};"

        cur = self._conn.cursor()

        try:
            cur.execute(query)
            row_count = cur.rowcount
            if row_count > 0:
                logging.info(f'row deleted from {table_name} table')
                self._conn.commit()
                return 1
            else:
                logging.error(f'row did not deleted from {table_name}')
                return -1
        except mySql_connector.Error as err:
            logging.error(f'query failed {query}, Error: {repr(err)}')
            return -1

    def update_row(self, table_name, item_id, update_values):
        """
        update() func, update record in a table.
        """

        # Prepare sql query for update record
        new_values = ""
        for key, value in update_values.items():
            new_values += f"{key}='{value}',"
        new_values = new_values[:-1]

        query = f"UPDATE {table_name} SET {new_values} WHERE id='{item_id}'"

        cur = self._conn.cursor()

        try:
            cur.execute(query)
            if cur.rowcount > 0:
                logging.debug(f'record updated in {table_name} table')
                self._conn.commit()
                return 1
            else:
                logging.error(f'query get failed {query}')
        except mySql_connector.Error as err:
            logging.error(f'query failed {query}, Error: {repr(err)}')
            return -1

    def is_connected(self):
        """
        return True if self._conn have mysql connection object else False'
        """
        if self._conn is None:
            return False
        else:
            return True

    def drop_table(self,table_name):
        if self.check_table_exist(table_name):
            query = f"DROP TABLE {table_name}"
            cur = self._conn.cursor()
            cur.execute(query)

            if cur.rowcount > 0:
                logging.debug(f'{table_name} table deleted successfully')
                return 1
            else:
                logging.error(f'query get failed {query}, table not deleted')
                return -1
        else:
            logging.error(f'{table_name} table already exist')
            return -1


    def close_conn(self):
        """
        close the Database connection from mysql server.
        """
        self._conn.close()
