#-*- coding: utf-8 -*-
import os
import hashlib
import sys
import zlib
import StringIO
import scanmod

VirusDB = [] #악성코드 패턴은 모두 virus.db에 존재함
vdb =[] #가공된 악성코드 DB가 저장된다
vsize = [] #악성코드의 파일크기만 저장한다.

#KMD파일 복호화.
def DecodeKMD(fname) :
    try :
        fp = open(fname, 'rb') #복호화 대상 파일을 연다.
        buf = fp.read()
        fp.close()

        buf2 = buf[:-32] #암호화 내용을 분리한다.
        fmd5 = buf[-32:] #MD5를 분리한다.

        f = buf2
        for i in range(3) : #암호화 내용의 MD5를 구한다.
            md5 = hashlib.md5()
            md5.update(f)
            f = md5.hexdigest()

        if f != fmd5 : #위 결과와 파일에서 분리된 MD5가 같은가?
            raise SystemError

        buf3 = ''
        for c in buf2[4:] : #0xFF로 XOR한다
            buf3 += chr(ord(c) ^ 0xFF)

        buf4 = zlib.decompress(buf3) #압축해제
        return buf4 #성공했다면 복호화 내용 리턴
    except :
        pass

    return None #오류가있다면 None 리턴

#virus.db파일에서 악성코드 패턴을 읽는다.
def LoadVirusDB() :
    buf = DecodeKMD('C:\\Users\\rkdud\\Desktop\\1\\virus.kmd')#악성 코드 패턴을 복호화한다.
    fp = StringIO.StringIO(buf)

    while True :
        line = fp.readline() #악성코드 패턴을 한 줄 읽는다.
        if not line : break

        line = line.strip()
        VirusDB.append(line) #악성코드 패턴을 Virus DB에 ㅜ가한다.
    fp.close() #악성코드 패턴 파일을 닫는다.

#VirusDB를 가공하여 vdb에 저장한다.
def MakeVirusDB() :
    for pattern in VirusDB :
        t =[]
        v=pattern.split(':') #세미콜론을 기준으로 자른다
        t.append(v[1]) #MD5해시를 저장한다.
        t.append(v[2]) #악성코드 이름 저장
        vdb.append(t) #최종 vdb에 저장

        size = int(v[0]) #악성코드 파일 크기
        if vsize.count(size) == 0 : #이미 파일크기가 등록되었나?
            vsize.append(size)



if __name__ == '__main__' :
    LoadVirusDB()  # 악성코드 패턴을 파일에서 읽는다
    MakeVirusDB()  # 악성코드 DB를 가공

    # 커맨드라인으로 악성코드를 검사할수있게 한다
    # 커맨드 라인의 입력방식을 체크
    if len(sys.argv) != 2:
        print 'Usage :virus.py [file]'
        exit(0)

    fname = sys.argv[1]  # 악성코드 검사 대상 파일

    ret, vname = scanmod.ScanMD5(vdb, vsize, fname)
    if ret == True:
        print '%s : %s' % (fname, vname)
        os.remove(fname)  # 파일을 삭제해서 치료
    else:
        print '%s : ok' % (fname)

