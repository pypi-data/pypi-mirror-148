# 用于启动时加载所有的数据表实例
instance = dict()

class DbBase(object):

    # 数据库只初始化一次

    def __new__(cls, env=None, db_name=None):

        if db_name is None:
            raise Exception('db_name为None，无法初始化数据库，请指定db_name')

        if instance.get(db_name) is not None:
            return instance.get(db_name)
        else:
            obj = super().__new__(cls)
            if env is None:
                raise Exception('环境变量为空，数据库初始化失败')

            obj.tableConfs = cls._getTableConfs(db_name)
            obj.dbConConf = cls._getDbConConf(db_name,env)
            instance.update({db_name: obj})
            return obj

    @classmethod
    def _getTableConfs(cls, db_name):

        '''获取数据库表实例配置'''

        pass

    @classmethod
    def _getDbConConf(cls, db_name, env):

        '''获取数据库配置'''

        pass

if __name__ == '__main__':
    pass
