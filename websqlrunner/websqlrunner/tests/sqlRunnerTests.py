import module
import unittest
from unittest import TestCase
from core.sqlRunner import *
from core.dbConnection import *


class SqlRunnerTests(TestCase):

    def setUp(self):
        self.dbConnection = DbConnection("bdConnection", "dbConnection", "server", "dbName",
                                         "username", "password")
        self.sqlRunner = SqlRunner(self.dbConnection)

    def test_init_with_none_argument_should_raise_value_error(self):
        self.assertRaises(ValueError, self.sqlRunner.run, None)

if __name__ == '__main__':
    unittest.main()
