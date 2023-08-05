import time
import os
import psutil

class Client(object):

    client_open_interval = 5

    @classmethod
    def client_exist(cls,client_path,start_type=1,proc_remark=None):

        '''检查客户端是否存在'''

        procs = cls.get_client_procs(client_path,start_type,proc_remark)
        if len(procs) > 0:
            return True
        return False

    @classmethod
    def open_client(cls,client_path,start_type=1,proc_remark=None):

        '''打开客户端'''

        if start_type == 1:
            os.system('taskkill /f /im {}'.format(os.path.basename(client_path)))
        else:
            if cls.client_exist(client_path,proc_remark):
                cls.close_client(client_path,start_type,proc_remark)

        if start_type == 1:
            os.startfile(client_path)
        elif start_type == 2:
            path_list = client_path.split('/')
            file_path = '\\'.join(path_list[:-1])
            os.system(r'cd / && %s && cd  %s && START %s' % (path_list[0], file_path, path_list[-1]))
        elif start_type == 3:
            path_list = client_path.split('/')
            file_path = '\\'.join(path_list[:-1])
            os.system(r'cd / && %s && cd  %s && START %s -proc_remark %s' % (
                path_list[0], file_path, path_list[-1], proc_remark))
        time.sleep(0.1)

    @classmethod
    def get_client_procs(cls,client_path,start_type=1,proc_remark=None):

        procs = list()
        for proc in psutil.process_iter():
            try:
                if os.path.normcase(proc.exe()) == os.path.normcase(client_path):
                    if start_type == 3:
                        if proc._proc.cmdline()[2] == proc_remark:
                            procs.append(proc)
                            break
                    else:
                        procs.append(proc)
                        break
            except:
                pass
        return procs

    @classmethod
    def close_client(cls,client_path,start_type=1,proc_remark=None):

        if start_type == 1:
            os.system('taskkill /f /im {}'.format(os.path.basename(client_path)))
        else:
            procs = cls.get_client_procs(client_path,start_type,proc_remark)
            for proc in procs:
                command = 'taskkill -f -pid {}'.format(proc.pid)
                os.popen(command)
                time.sleep(0.1)