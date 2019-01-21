#-*- coding: utf-8 -*-
import os
import hashlib
import sys
import zlib

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

if __name__ == '__main__' :
    if len(sys.argv)!= 2:
        print 'Usage : 3_2.py [file]'
        exit(0)

    fname = sys.argv[1] #암호화 대상 파일
    print(DecodeKMD(fname))