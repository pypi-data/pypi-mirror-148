import pymysql
from dbutils.pooled_db import PooledDB
import warnings

warnings.filterwarnings('ignore')
instance = dict()

class DbCon:

    # 数据库连接只初始化一次

    def __new__(cls, dbConConf):

        if instance.get(dbConConf['database']) is not None:
            return instance.get(dbConConf['database'])

        obj = object.__new__(cls)
        obj._pool = PooledDB(
            creator=pymysql,
            maxconnections=dbConConf['maxactive'],
            mincached=dbConConf['minidle'],
            maxcached=dbConConf['maxidle'],
            host=dbConConf['host'],
            port=dbConConf['port'],
            user=dbConConf['username'],
            database=dbConConf['database'],
            password=dbConConf['password'],
            charset=dbConConf['charset'],
            blocking=False,
            autocommit=bool(dbConConf['autocommit'] != 0)
        )
        instance[dbConConf['database']]=obj

        return obj

    def selectall(self, sql, values=()):
        connection = self._pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, values)
            result = cursor.fetchall()
            if len(result) == 0:
                return []
            else:
                return result
        finally:
            connection.close()
            cursor.close()

    def selectone(self, sql, values=()):
        connection = self._pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, values)
            return cursor.fetchone()
        finally:
            connection.close()
            cursor.close()

    def insert(self, sql, values=(), commit=False):
        connection = self._pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, values)
            lastid = cursor.lastrowid
            if commit:
                connection.commit()
            return lastid
        except Exception as e:
            if commit:
                connection.rollback()
            raise e
        finally:
            connection.close()
            cursor.close()

    def insertmany(self, sql, values=(), commit=False):
        connection = self._pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.executemany(sql, values)
            rowcount = cursor.rowcount
            if commit:
                connection.commit()
            return rowcount
        except Exception as e:
            if commit:
                connection.rollback()
            raise e
        finally:
            connection.close()
            cursor.close()

    def execute(self, sql, values=(), commit=False):
        connection = self._pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, values)
            rowcount = cursor.rowcount
            if commit:
                connection.commit()
            return rowcount
        except Exception as e:
            if commit:
                connection.rollback()
            raise e
        finally:
            connection.close()
            cursor.close()

