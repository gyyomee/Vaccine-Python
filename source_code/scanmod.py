#-*- coding: utf-8 -*-
import os
import hashlib

#특정 위치 검색법을 이용하여 악성코트 검사
def ScanStr(fp, offset, mal_str) :
    size = len(mal_str) #악성코드 진단 문자열의 길이

    #특정 위치에 악성코드 진단 문자열이 있는지 체크
    fp.seek(offset) #악성코드 문자열이 있을 곳으로 예상하는 위치로 이동
    buf = fp.read(size) #악성코드 문자열의 길이만큼 읽기

    if buf == mal_str :
        return True #악성코드 발견
    else :
        return False #악성코드 미발견

# 악성코드를 검사한다.
def SearchVDB(vdb, fmd5) :
    for t in vdb :
        if t[0] == fmd5 : #MD5 해시가 같은지 비교
            return True, t[1] #악성코드 이름을 함께 리턴
    return False, '' #악성코드가 발견되지 않음

# 악성코드를 검사한다.
def ScanVirus(vdb, vsize, sdb, fname) :
    #MD5해시를 이용하여 악성코드를 검사
    ret, vname = ScanMD5(vdb, vsize, fname)
    if ret == True :
        print 'MD5사용'
        return ret, vname

    #특정 위치 검색법을 이용하여 악성코드 검사
    fp = open(fname, 'rb')
    for t in sdb :
        if ScanStr(fp, t[0], t[1]) == True :
            ret = True
            vname = t[2]
            print 'Scan사용'
            break
    fp.close()
    return ret, vname

#MD5를 이용하여 악성코드 검사
def ScanMD5(vdb, vsize, fname):
    ret = False #악성코드 발견 유무
    vname = '' #발견된 악성코드명

    size = os.path.getsize(fname)  # 검사 대상 파일 크기를 구한다.
    if vsize.count(size):  # 파일크기가 일치하면
        fp = open(fname, 'rb')  # 바이너리 모드로 읽기
        buf = fp.read()
        fp.close()

        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()

        ret, vname = SearchVDB(vdb, fmd5)  # 악성코드 검사.

    return ret, vname
