import unittest


from sql_db import SqlDB


class TestSqlDB(unittest.TestCase):

    def setUp(self):
        self.db_conn = SqlDB('sachin','passwrd#321','localhost','crypto_db')

    def tearDown(self):
        self.db_conn.close_conn()

    # test mysql connection using correct credentials
    def test_sql_connection_with_right_credentials(self):
        db_conn = SqlDB('sachin','passwrd#321','localhost','crypto_db')
        expected = True
        real = db_conn.is_connected()
        self.assertEqual(real, expected)

    # test mysql connection using wrong credentials
    def test_sql_connection_with_wrong_credentials(self):
        db_conn1 = SqlDB('sachin123','passwrd#321','localhost','crypto_db')
        db_conn2 = SqlDB('sachin', 'passwrd#3210', '', '')
        db_conn3 = SqlDB('sachin', '', '', '')

        self.assertEqual(False, db_conn1.is_connected())
        self.assertEqual(False, db_conn2.is_connected())
        self.assertEqual(False, db_conn3.is_connected())

    # testing create_table() func, with right syntax, 'table_name' & 'columns'
    def test_create_table_with_right_args(self):
        table_name = 'testing_table'
        columns = ['dummy_1','dummy_2','dummy_3']
        success_or_error = self.db_conn.create_table(table_name,columns)
        success = 1

        self.assertEqual(True,self.db_conn.check_table_exist(table_name))
        self.assertEqual(success, success_or_error)

        self.db_conn.drop_table(table_name)

    # testing create_table() func, with incorrect syntax, 'table_name' & 'columns'
    def test_create_table_with_wrong_args(self):
        error = -1

        table_name1 = ''
        columns1 = ['dummy_1','','dummy_3']
        success_or_error1 = self.db_conn.create_table(table_name1, columns1)

        table_name2 = 'test_create_table2'
        columns2 = []
        success_or_error2 = self.db_conn.create_table(table_name2, columns2)

        table_name3 = 'already_exist_table'
        columns3 = ['dummy_1','dummy_2','12_']
        success_or_error3 = self.db_conn.create_table(table_name3, columns3)

        self.assertEqual(False,self.db_conn.check_table_exist(table_name1))
        self.assertEqual(False, self.db_conn.check_table_exist(table_name2))
        self.assertEqual(error, success_or_error1)
        self.assertEqual(error, success_or_error2)
        self.assertEqual(error, success_or_error3)

    # test insert_into_table() func, by inserting correct rows.
    def test_insert_record_into_table_with_correct_col_order(self):
        success = 1
        table_name = "test_table"
        item_id = "1001"
        record = [item_id,"val_1","val_2","val_2"]

        success_or_error3 = self.db_conn.insert_into_table(table_name,[record])
        record_from_db = self.db_conn.read_rows(table_name,item_id)[0].values()

        self.assertEqual(success_or_error3,success)
        self.assertEqual(list(record_from_db).sort(), record.sort())

        self.db_conn.delete_row(table_name,item_id)

    def test_insert_record_into_table_with_duplicat_id(self):
        error = -1
        table_name = "test_table"
        item_id = "1"
        record = [item_id,"val_11","val_22","val_22"]
        unique_item_count = 1

        success_or_error = self.db_conn.insert_into_table(table_name,[record])
        record_from_db = self.db_conn.read_rows(table_name,item_id)

        self.assertEqual(success_or_error,error)
        self.assertEqual(unique_item_count,len(record_from_db))


    def test_delete_record_from_table_with_right_id(self):
        # setup
        table_name = "test_table"
        item_id = "101"
        record = [item_id, "val_1", "val_2", "val_2"]
        self.db_conn.insert_into_table(table_name, [record])
        success = 1

        success_or_error = self.db_conn.delete_row(table_name,item_id)
        result = self.db_conn.read_rows(table_name,item_id)
        print(result)

        self.assertEqual(success_or_error,success)
        self.assertNotEqual(None, result)

        self.db_conn.delete_row(table_name, item_id)

    def test_delete_record_from_table_with_absent_id(self):
        error = 1
        table_name = 'test_table'
        item_id = 'absent_id'

        before_deletion_rows = self.db_conn.read_rows(table_name)
        success_or_error = self.db_conn.delete_row(table_name,item_id)
        after_deletion_rows = self.db_conn.read_rows(table_name)

        self.assertEqual(before_deletion_rows,after_deletion_rows)













if __name__ == "__main__":
    unittest.main()
