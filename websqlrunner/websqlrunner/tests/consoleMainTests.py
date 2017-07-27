import module
import unittest

from unittest import TestCase
from unittest.mock import MagicMock, Mock
from console.main import *
from core.sqlRunner import *


class MainTests(TestCase):

    def setUp(self):
        self.dbConnection = DbConnection("name", "desc", "server", "database", "user", "password")
        self.sql = "select 1"

    def test_main_none_sql_query_raise_value_error(self):
        self.assertRaises(ValueError, main, ["a"], None)

    def test_main_sql_query_must_be_string(self):
        self.assertRaises(TypeError, main, ["a"], object())

    def test_main_connection_strings_none_raise_value_error(self):
        self.assertRaises(ValueError, main, None, self.sql)

    def test_main_connection_strings_empty_raise_value_error(self):
        self.assertRaises(ValueError, main, [], self.sql)

    def test_main_connection_string_must_be_a_list_type_error_otherwise(self):
        self.assertRaises(TypeError, main, "hello", self.sql)

    def test_main_is_parallel_should_be_of_type_bool(self):
        self.assertRaises(TypeError, main, ["a"], self.sql, "not bool")

    def test_main_should_invoke_run_on_parallel(self):
        pass

    def test_main_should_invoke_run_sequentially(self):
        sqlRunner = SqlRunner(self.dbConnection)
        sqlRunner.run = MagicMock(return_value=0)
        SqlRunner.from_sql_server_connection_string = MagicMock(return_value=sqlRunner)
        conn_strings = ["c1", "c2"]
        main(conn_strings, self.sql)
        self.assertEqual(sqlRunner.run.call_count, len(conn_strings))

    def test_main_should_start_a_new_thread_per_connection(self):

        def create_sqlrunner(connection_string):
            connection = DbConnection(connection_string, "", "", "", "", "")
            sqlrunner = SqlRunner(connection)
            sqlrunner.run = MagicMock(return_value=0)
            return sqlrunner

        SqlRunner.from_sql_server_connection_string = MagicMock(side_effect=create_sqlrunner)
        threads = []

        def create_thread(sqlrunner, sql, thread_id, name, counter):
            sqlrunner_thread = SqlRunnerThread(thread_id, name, counter, sqlrunner, sql)
            sqlrunner_thread.start = MagicMock()
            sqlrunner_thread.join = MagicMock()
            threads.append(sqlrunner_thread)
            return sqlrunner_thread

        SqlRunnerThread.from_sqlrunner = Mock(side_effect=create_thread)
        conn_strings = ["c1", "c2"]
        main(conn_strings, self.sql, True)
        for t in threads:
            t.start.assert_called_once_with()
            t.join.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
