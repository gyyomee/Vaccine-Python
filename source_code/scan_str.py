#-*- coding: utf-8 -*-

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

#파일을 열어서 악성코드 삭제
fp = open('C:\\Users\\rkdud\\Desktop\\1\\eicar.txt', 'rb')
print ScanStr(fp, 0, 'X5O')
fp.close()