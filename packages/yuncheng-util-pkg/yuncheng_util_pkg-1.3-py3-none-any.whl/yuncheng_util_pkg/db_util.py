import MySQLdb as mdb
class GetDbData:
    def __init__(self,host,name,pw,db):
        self.host = host
        self.name = name
        self.pw = pw
        self.db = db
    def connect(self):
        connectResult = 0
        try:
            self.con = mdb.connect(host=self.host,user=self.name,passwd=self.pw,db=self.db);
            if self.con is not None:
                print('db连接已经建立')
            else:
                print('db连接无法建立')
                connectResult = 1
        except Exception as e:
            connectResult = 1
            print('db连接出现问题，{}'.format(e))
        return connectResult
    def excuteSql(self,sql):
        try:
            connect = self.connect()
            if connect == 0:
                cur = self.con.cursor()
                # 创建一个数据表 writers(id,name)
                cur.execute(sql)
                rows = cur.fetchall()
            else:
                print('db连接出问题，该sql不能执行!')
                rows = None
        except Exception as e:
            rows = None
            print('something wrong happened:{}'.format(e))
        finally:
            if hasattr(self,'con') is True:
                self.con.close()
                print('db连接已经关闭')
            else:
                print('由于连接不存在，db无需关闭连接')
        print('sql执行结果返回')
        return rows

    def excuteManySql(self,sqls):
        results = []
        try:
            connect = self.connect()
            if connect == 0:
                cur = self.con.cursor()
                for sql in sqls:
                    cur.execute(sql)
                    rows = cur.fetchall()
                    results.append(rows)
            else:
                print('db连接出问题，该sql不能执行!')
                rows = None
        except Exception as e:
            rows = None
            print('something wrong happened:{}'.format(e))
        finally:
            if hasattr(self,'con') is True:
                self.con.close()
                print('db连接已经关闭')
            else:
                print('由于连接不存在，db无需关闭连接')
        print('sql执行结果返回')
        return results






