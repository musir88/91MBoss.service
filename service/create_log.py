import os
import codecs


f = open('user.txt', encoding="utf-8")
prot = f.read()
f.close()





content = ''


fo = codecs.open("2022-06-09.log", "a", 'utf-8')
fo.write(content)
fo.close()