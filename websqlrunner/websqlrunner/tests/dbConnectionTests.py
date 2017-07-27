import module
import unittest
from unittest import TestCase
from core.dbConnection import DbConnection


class SqlRunnerTests(TestCase):

    def test_db_connection_create_from_connection_string(self):
        conString = "Data Source=ra-labs-01.database.windows.net;Initial Catalog=DevAzureAdmin;" \
                    "User id=ra-labs-01-admin@ra-labs-01;Password=RA123456!;Connection Timeout=1800"
        dbConnection = DbConnection.from_connection_string(conString)
        self.assertEqual(dbConnection.dbServer, "ra-labs-01.database.windows.net")
        self.assertEqual(dbConnection.dbName, "DevAzureAdmin")
        self.assertEqual(dbConnection.username, "ra-labs-01-admin@ra-labs-01")
        self.assertEqual(dbConnection.password, "RA123456!")
        self.assertEqual(dbConnection.timeout, 1800)

    def test_db_connection_create_from_connection_string_strip(self):
        conString = "Data Source= ra-labs-01.database.windows.net ;Initial Catalog= DevAzureAdmin ;" \
                    "User id= ra-labs-01-admin@ra-labs-01 ;Password = RA123456! ;" \
                    "Connection Timeout= 1800 "
        dbConnection = DbConnection.from_connection_string(conString)
        self.assertEqual(dbConnection.dbServer, "ra-labs-01.database.windows.net")
        self.assertEqual(dbConnection.dbName, "DevAzureAdmin")
        self.assertEqual(dbConnection.username, "ra-labs-01-admin@ra-labs-01")
        self.assertEqual(dbConnection.password, "RA123456!")
        self.assertEqual(dbConnection.timeout, 1800)

    def test_db_connection_to_sql_server_string(self):
        server, dbname, user, password, timeout = "server", "dbname", "admin", "p@ssw0rd", 100
        dbConnection = DbConnection("", "", server, dbname, user, password, timeout)

        expected = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=server;DATABASE=dbname;UID=admin;PWD=p@ssw0rd"
        self.assertEqual(expected, dbConnection.to_sqlserver_string())

if __name__ == '__main__':
    unittest.main()
