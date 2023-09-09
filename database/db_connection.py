import psycopg2


class DataBaseConnection:

    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def execute(self, qwery, *args):
        with self.connection.cursor() as cursor:
            cursor.execute(qwery, args)
            self.connection.commit()

    def fetchone(self, qwery, *args):
        with self.connection.cursor() as cursor:
            cursor.execute(qwery, args)
            return cursor.fetchone()

    def close(self):
        self.connection.close()
