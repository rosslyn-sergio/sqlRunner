

class DbConnection(object):
    def __init__(self, name, description, db_server, db_name, username, password,
                 timeout=10):
        self.name = name
        self.description = description
        self.dbServer = db_server
        self.dbName = db_name
        self.username = username
        self.password = password
        self.timeout = timeout

    @classmethod
    def from_connection_string(cls, connection_string):
        conn = connection_string
        parts = conn.strip().split(';')

        def split_part(p):
            return tuple(map(str.strip, p.split('=')))

        d = dict(map(split_part, parts))
        return DbConnection(name="SqlServerConnection", description=None,
                            db_server=d["Data Source"], db_name=d["Initial Catalog"],
                            username=d["User id"], password=d["Password"],
                            timeout=int(d["Connection Timeout"]))

    def to_sqlserver_string(self):
        return "DRIVER={ODBC Driver 13 for SQL Server};SERVER=" + self.dbServer + \
               ";DATABASE=" + self.dbName + \
               ";UID=" + self.username + \
               ";PWD=" + self.password
    
    def to_sqlserver_string_tds_driver(self):
         return "DRIVER=FreeTDS;SERVER=" + self.dbServer + \
               ";DATABASE=" + self.dbName + \
               ";UID=" + self.username + \
               ";PWD=" + self.password + \
               ";TDS_Version=8.0;"



    def to_my_sql_string(self):
        raise NotImplementedError()
