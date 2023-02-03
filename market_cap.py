#가상 환경 만드는법 python -m venv myenv 
#실행 시키는법 .\myenv\Scipts\activate 

#https://finance.naver.com/sise/sise_market_sum.naver
import os
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화 

url="https://finance.naver.com/sise/sise_market_sum.naver?&page="
#1. 페이지 이동 
browser.get(url)

#조회 항목 초기화 
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): #체크된 상태인지 확인
        checkbox.click()# 체크 해제 

#조회 황목 설정 (원하는 항목 리스트에 저장 )
items_to_select=['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent=checkbox.find_element(By.XPATH, '..')#부모 엘리먼트 찾게 된다 td 엘레먼트가 parent 로 들간다
    label = parent.find_element(By.TAG_NAME,'label')
    #print(label.text)#이름확인
    if label.text in items_to_select:
        checkbox.click() #선택하려는것들 체크 해라 여기서 
        
# 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]') # // 전체 html 문서에서 찾겠따 
btn_apply.click()

for idx in range(1,41):#1~40 까지
    #사전 작업: 페이지 이동 
    browser.get(url + str(idx)) 
    
    #데이터 추출 
    df = pd.read_html(browser.page_source)[1]
    #우리는 인덱스 1 데이터 추출할거임
    # 없는 데이터 값 지우는밥
    #row 기준
    df.dropna(axis='index', how='all',inplace=True) # 줄 전체가 데이터 없는경우에 지워 라는 명령문 지운게 바로 반영
    #column 기준 
    df.dropna(axis='columns',how='all',inplace=True)
    if len(df) ==0:
        break#만약에 페이지수가 내가 정한것보다 적으면 반복문 나가야 되니까
    
    #파일저장 1페이지에서만 헤더 넣고 다음 페이지 부터는 헤더 제외
    f_name = 'sise.csv'
    if os.path.exists(f_name):#파일이 있다면 헤더 부분 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a',header=False) # mode 는 어펜드 
    else: #파일이 없는경우 헤더를 포함시켜야된다
        df.to_csv(f_name,encoding='utf-8-sig',index=False)

    print(f'{idx} 페이지 완료!')


browser.quit()#브라우저 종료
