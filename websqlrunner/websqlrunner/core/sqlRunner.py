import pyodbc as py
import pymssql as pym
from .dbConnection import DbConnection
import os
#os.environ['TDSDUMP'] = 'stdout'


class SqlRunner(object):
    def __init__(self, db_connection):
        if not isinstance(db_connection, DbConnection):
            raise TypeError(db_connection)

        self._dbConnection = db_connection

    @classmethod
    def from_sql_server_connection_string(cls, connection_string):
        connection = DbConnection.from_connection_string(connection_string)
        return SqlRunner(connection)

    def run(self, sql):
        if not sql:
            raise ValueError()
        try:
            dbc = self._dbConnection
            conn = pym.connect(dbc.dbServer, dbc.username,dbc.password,dbc.dbName)
           # conn = pyo.connect(self._dbConnection.to_sqlserver_string_tds_driver())
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
        except pym.Error as error:
            conn.rollback()
            conn.close()
            return 1, error
        
        return 0, None

    def validate(self, sql):
        if not sql:
            raise ValueError()

    def get_connection(self):
        return str(self._dbConnection.toString())
