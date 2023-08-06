from auto_rpa.utils.mysql_utils.db_con import DbCon
import datetime
import decimal
import math


class SerializeEncoder:
    @classmethod
    def format_dict(cls, dt):
        result = {k: cls.format_item(dt[k]) for k in dt}
        return result

    @classmethod
    def format_list(cls, dt):
        result = [cls.format_item(item) for item in dt]
        return result

    @classmethod
    def format_item(cls, dt):
        if isinstance(dt, dict):
            return cls.format_dict(dt)
        if isinstance(dt, list):
            return cls.format_list(dt)
        if isinstance(dt, decimal.Decimal):
            return float(dt)
        if isinstance(dt, datetime.datetime):
            return datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
        return dt

# instance = dict()

class DbTable():

    # 表实例只初始化一次

    # def __new__(cls, table_name=None, table_conf={}, db_con_conf={}):
    #
    #     if instance.get(table_name) is not None:
    #         return instance.get(table_name)
    #     else:
    #         obj = super().__new__(cls)
    #         instance.update({table_name: obj})
    #         return obj

    def __init__(self, table_name=None, table_conf={}, db_con_conf={}):

        self.table_name = table_name
        self.DBHelper = DbCon(db_con_conf)
        self.database = self.DBHelper._pool._kwargs['database']
        self.table_conf = table_conf

    def insertTb(self, dbparams):

        '''插入数据库'''

        many = bool(type(dbparams).__name__ == 'list')
        if not many:
            dbparams = [dbparams]
        if dbparams is None or len(dbparams) == 0:
            return None

        keys = list()
        keylist = self.getKeyList()
        symbels = list()
        for key in dbparams[0]:
            if key in keylist and key not in keys:
                keys.append(key)
                symbels.append('%s')

        manyvalues = list()
        for params in dbparams:
            values = list()
            for key in keys:
                values.append(params[key])
            manyvalues.append(values)

        sql = 'INSERT IGNORE INTO ' + self.table_name + ' (' + ','.join(keys) + ')' \
              + ' VALUES (' + ', '.join(symbels) + ')'
        if len(manyvalues) == 1:
            return self.DBHelper.insert(sql, manyvalues[0])
        else:
            return self.DBHelper.insertmany(sql, manyvalues)

    def updateTb(self, setparams, conditionparams={}):

        '''用于更新数据'''

        symbels = list()
        values = list()

        for key in setparams:
            if key in self.getKeyList():
                symbels.append(key + ' = %s')
                values.append(setparams[key])

        sql = 'UPDATE ' + self.table_name + ' SET ' + ','.join(symbels) + ' WHERE '
        wherestr, updatevalues = self.getWhereStr(conditionparams)
        values.extend(updatevalues)
        sql += wherestr

        return self.DBHelper.execute(sql, values)

    def deleteBy(self, params):

        '''用于删除数据'''

        id = 0
        if isinstance(params,list):
            for param in params:
                sql = 'DELETE FROM ' + self.table_name + ' WHERE '
                wherestr, values = self.getWhereStr(param)
                sql += wherestr
                id = self.DBHelper.execute(sql, values)
        else:
            sql = 'DELETE FROM ' + self.table_name + ' WHERE '
            wherestr, values = self.getWhereStr(params)
            sql += wherestr

            id = self.DBHelper.execute(sql, values)

        return id

    def listBy(self, params, fields=None):

        '''按条件查询多行'''

        field = self.getField(fields)
        sql = "SELECT " + field + " FROM " + self.table_name + " WHERE "
        if params is None:
            params = dict()
        wherestr, values = self.getWhereStr(params)
        sql += wherestr

        if params.get('orderbys'):
            sql += ' ORDER BY ' + params['orderbys']

        if params.get('orderby'):
            sql += ' ORDER BY ' + params['orderby'] + ' ' + params.get('asc', 'asc')
        if params.get('groupby'):
            sql += ' GROUP BY ' + params['groupby']
        if not params.get('limit') is None:
            sql += ' limit ' + str(params.get('offset', 0)) + ', ' + str(params.get('limit', 20))

        return self.DBHelper.selectall(sql, values)

    def getOneBy(self, params, fields=None):

        '''获取一行'''

        field = self.getField(fields)
        sql = "SELECT " + field + " FROM " + self.table_name + " WHERE "
        if params is None:
            params = dict()
        wherestr, values = self.getWhereStr(params)
        sql += wherestr

        return self.DBHelper.selectone(sql, values)

    def executeSql(self, params):

        '''完全自定义sql语句执行'''

        conditions = self.table_conf['conditions']
        values = []
        for key, valuelist in params.items():
            conditions_sql = conditions[key].get('conditions_sql')
            for i in valuelist:
                values.append(i)
        return self.DBHelper.selectall(conditions_sql % tuple(values))

    def insertUpdate(self, all_data, unique_keys=[], insert=False, update=False, id_key='id'):

        '''批量插入更新,注意条件中有空值的情况处理'''

        if isinstance(all_data,dict):
            all_data = [all_data]
        if len(all_data) == 0:
            return 0,0

        def MyEncode(x):
            if isinstance(x, datetime.datetime):
                return x.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return x

        insert_count = 0
        update_count = 0

        group_num = math.ceil(len(all_data) / 300)
        for n in range(group_num):
            min = n * 300
            max = (n + 1) * 300
            if max >= len(all_data):
                max = len(all_data)
            data = all_data[min:max]

            records = self.select_batch(data, unique_keys)
            record_dict = {tuple(MyEncode(record[k]) for k in unique_keys): record for record in records}

            update_data = list()
            insert_data = list()
            for d in data:
                key = tuple(d[k] for k in unique_keys)
                if key in record_dict:
                    d['id'] = record_dict[key]['id']
                    update_data.append(d)
                else:
                    insert_data.append(d)
            if insert:
                if len(insert_data):
                    tmp_insert_count = self.insert_batch(insert_data)
                    insert_count += tmp_insert_count
            if update:
                if len(update_data):
                    tmp_update_count = self.update_batch(update_data,id_key)
                    update_count += tmp_update_count

        return insert_count, update_count

    def select_batch(self, dt_list, keys):

        dt_list = SerializeEncoder.format_list(dt_list)
        sqls = []
        for dt in dt_list:
            sqls.append('select * from %s where ' % self.table_name + ' and '.join((k + '= %r' % dt[k]) for k in keys))
        sql = '\r\nUNION \r\n'.join(sqls)

        res = self.DBHelper.selectall(sql)

        return res

    def insert_batch(self, dt_list, ignore=False):

        dt_list = SerializeEncoder.format_list(dt_list)
        symb_values = []
        values = []
        if len(dt_list) == 0:
            return None, None
        for dt in dt_list:
            symb_values.append('(%s' + ',%s' * (len(dt_list[0]) - 1) + ')')
            values.extend([dt.get(key, 'null') for key in dt_list[0]])
        ignore_str = 'ignore' if ignore else ''
        sql = 'insert %s into %s(%s) values %s' % (ignore_str, self.table_name, ','.join(dt_list[0].keys()), ','.join(symb_values))

        count = self.DBHelper.execute(sql, values)

        return count

    def update_batch(self, dt_list, id_key):

        """将dt_list的update_keys列批量进行更新,id_key是dt_list中唯一的key,用来找到数据库中的对应行"""

        update_keys = set(dt_list[0].keys())
        update_keys.remove('id')
        dt_list = SerializeEncoder.format_list(dt_list)
        sub_sqls = []
        for k in update_keys:
            sql_update = '%s = CASE %s' % (k, id_key)
            for dt in dt_list:
                sql_update += '\r\n WHEN %r THEN %r' % (dt[id_key], dt[k])
            sql_update += '\r\n END\r\n'
            sub_sqls.append(sql_update)
        ids = [str(d[id_key]) for d in dt_list]
        sql = 'UPDATE %s SET ' % self.table_name + ','.join(sub_sqls) \
              + ' WHERE ' + id_key + ' IN (' + ','.join(ids) + ');'

        count = self.DBHelper.execute(sql)

        return count

    def getKeyList(self):

        '''获取表所有字段'''

        sql = '''Select COLUMN_NAME 
           from INFORMATION_SCHEMA.COLUMNS  
           Where table_schema = %s and table_name = %s
           '''

        fields = self.DBHelper.selectall(sql, [self.database, self.table_name])
        return [field['COLUMN_NAME'] for field in fields]

    def getField(self, fields):

        '''获取字段'''

        field = '*'
        if fields is not None and len(fields) > 0:
            field = ','.join(fields)
        return field

    def getWhereStr(self, params):

        '''组织sql拼接'''

        wherestr = '1'
        values = list()

        if len(params) == 0:
            return wherestr, values

        conditions = self.table_conf['conditions']
        for key, value in params.items():

            if key not in conditions.keys():
                continue
            if value is None:
                continue
            conditionstype = conditions[key]['conditionstype']
            conditions_relation = conditions[key]['conditions_relation']
            conditions_relation = 'AND' if conditions_relation == 1 else "OR"
            # 可以没有
            conditions_sql = conditions[key].get('conditions_sql')
            conditions_field = conditions[key].get('conditions_field')
            conditions_field = key if conditions_field is None else conditions_field
            bool_mark = conditions[key].get('bool_mark')
            bool_mark = ' ' if bool_mark is None else bool_mark

            if conditionstype == 1:

                wherestr += ' %s %s ' % (conditions_relation, conditions_field) + bool_mark + '= %s'
                values.append(value)

            elif conditionstype == 2:

                symbels = list()
                for field in value:
                    symbels.append('%s')
                    values.append(field)
                wherestr += ' %s %s ' % (conditions_relation, conditions_field) + bool_mark + ' in (%s)' % ','.join(
                    symbels)

            elif conditionstype == 3:
                wherestr += ' %s ' % conditions_relation + conditions_sql
                if isinstance(value, list):
                    for i in value:
                        values.append(i)
                else:
                    values.append(value)

        return wherestr, values
