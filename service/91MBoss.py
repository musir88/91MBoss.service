import os
f = open('host.ini', encoding="utf-8")
prot = f.read()
f.close()

os.system('boss.exe runserver 0.0.0.0:'+str(prot)+' --noreload')
# input()

print('如果您是中国大陆公民请自行离开，此软件不允许中国大陆用户使用。')