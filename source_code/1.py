#-*- coding: utf-8 -*-
import os
import hashlib

fp=open('C:\\Users\\rkdud\\Desktop\\1\\eicar.txt','rb')  #바이너리 모드로 읽기
fbuf = fp.read()
fp.close()
if fbuf[0:3] == 'X5O': #파일의 앞 3Byte가 'X50'인가?
    print('Virus')
    os.remove('C:\\Users\\rkdud\\Desktop\\1\\eicar.txt') #파일을 삭제해서 치료
else:
    print('No Virus')

m = hashlib.md5()
m.update(fbuf)
fmd5 = m.hexdigest()

#EICAR Text 파일 MD5와 비교
if fmd5 =='44d88612fea8a8f36de82e1278abb02f' :
    print ('Virus')
    os.remove('C:\\Users\\rkdud\\Desktop\\1\\eicar.txt')
else:
    print('No virus')

