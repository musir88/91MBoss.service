import os
import configparser
config = configparser.ConfigParser() # 类实例化

path = r'Bot/host.ini'
config.read(path)
prot = config['base']['prot']


os.system('cd Bot && boss.exe runserver 0.0.0.0:'+str(prot)+' --noreload')

print('此软件不允许中国用户使用。')