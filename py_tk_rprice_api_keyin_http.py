# -*- coding: utf-8 -*-
import requests
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import xml.etree.ElementTree as etree
import time, datetime, os
import xmltodict

from tkinter import *

import tkinter.ttk as ttk
import tkinter.messagebox as msgbox  #메시지박스
from tkinter import filedialog  #서브모듈이라서, 파일선택 대화상자 모듈 불러옴 


    
root = Tk()
root.title("실거래가 API")
root.geometry("1600x640") # set the root dimensions
root.resizable(0, 0) # makes the root window fixed in size.                                        

mykey = "DwLaTWFhLDb2IefBfOYTWxPJ1IhcZ8OMsq5lNkQLxUiZS6Z2hf3Ezw25JlQXVg6Ul5poZk9zseag0Dlz%2Fxap7Q%3D%3D" #동규 key

def period(start_code, end_code):
    result = []
    start_YY = int(start_code[:4])
    start_MM = int(start_code[4:])

    end_YY = int(end_code[:4])
    end_MM = int(end_code[4:])    
    
    tmp_MM = start_MM
    tmp_YY = start_YY
 
    print(tmp_YY*100+tmp_MM) 
    print(end_YY*100+end_MM)
        
    while(tmp_YY*100+tmp_MM <= end_YY*100+end_MM):
        tmp_timecode = tmp_YY*100 + tmp_MM 
        
        result.append(tmp_timecode)
        tmp_MM = tmp_MM + 1
        
        if tmp_MM >= 13:
            tmp_MM = 1
            tmp_YY = tmp_YY + 1
  
    return result

def local_name(x):
    dic_name={'서울특별시': '11000', '서울특별시 종로구': '11110', '서울특별시 중구': '11140', '서울특별시 용산구': '11170', '서울특별시 성동구': '11200', '서울특별시 광진구': '11215', '서울특별시 동대문구': '11230', '서울특별시 중랑구': '11260', '서울특별시 성북구': '11290', '서울특별시 강북구': '11305', '서울특별시 도봉구': '11320', '서울특별시 노원구': '11350', '서울특별시 은평구': '11380', '서울특별시 서대문구': '11410', '서울특별시 마포구': '11440', '서울특별시 양천구': '11470', '서울특별시 강서구': '11500', '서울특별시 구로구': '11530', '서울특별시 금천구': '11545', '서울특별시 영등포구': '11560', '서울특별시 동작구': '11590', '서울특별시 관악구': '11620', '서울특별시 서초구': '11650', '서울특별시 강남구': '11680', '서울특별시 송파구': '11710', '서울특별시 강동구': '11740', '부산광역시': '26000', '부산광역시 중구': '26110', '부산광역시 서구': '26140', '부산광역시 동구': '26170', '부산광역시 영도구': '26200', '부산광역시 부산진구': '26230', '부산광역시 동래구': '26260', '부산광역시 남구': '26290', '부산광역시 북구': '26320', '부산광역시 해운대구': '26350', '부산광역시 사하구': '26380', '부산광역시 금정구': '26410', '부산광역시 강서구': '26440', '부산광역시 연제구': '26470', '부산광역시 수영구': '26500', '부산광역시 사상구': '26530', '부산광역시 기장군': '26710', '대구광역시': '27000', '대구광역시 중구': '27110', '대구광역시 동구': '27140', '대구광역시 서구': '27170', '대구광역시 남구': '27200', '대구광역시 북구': '27230', '대구광역시 수성구': '27260', '대구광역시 달서구': '27290', '대구광역시 달성군': '27710', '대구광역시 군위군': '27720', '인천광역시': '28000', '인천광역시 중구': '28110', '인천광역시 동구': '28140', '인천광역시 미추홀구': '28177', '인천광역시 연수구': '28185', '인천광역시 남동구': '28200', '인천광역시 부평구': '28237', '인천광역시 계양구': '28245', '인천광역시 서구': '28260', '인천광역시 강화군': '28710', '인천광역시 옹진군': '28720', '광주광역시': '29000', '광주광역시 동구': '29110', '광주광역시 서구': '29140', '광주광역시 남구': '29155', '광주광역시 북구': '29170', '광주광역시 광산구': '29200', '대전광역시': '30000', '대전광역시 동구': '30110', '대전광역시 중구': '30140', '대전광역시 서구': '30170', '대전광역시 유성구': '30200', '대전광역시 대덕구': '30230', '울산광역시': '31000', '울산광역시 중구': '31110', '울산광역시 남구': '31140', '울산광역시 동구': '31170', '울산광역시 북구': '31200', '울산광역시 울주군': '31710', '세종특별자치시': '36110', '경기도': '41000', '경기도 수원시': '41110', '경기도 수원시 장안구': '41111', '경기도 수원시 권선구': '41113', '경기도 수원시 팔달구': '41115', '경기도 수원시 영통구': '41117', '경기도 성남시': '41130', '경기도 성남시 수정구': '41131', '경기도 성남시 중원구': '41133', '경기도 성남시 분당구': '41135', '경기도 의정부시': '41150', '경기도 안양시': '41170', '경기도 안양시 만안구': '41171', '경기도 안양시 동안구': '41173', '경기도 부천시': '41190', '경기도 부천시 원미구': '41192', '경기도 부천시 소사구': '41194', '경기도 부천시 오정구': '41196', '경기도 광명시': '41210', '경기도 평택시': '41220', '경기도 동두천시': '41250', '경기도 안산시': '41270', '경기도 안산시 상록구': '41271', '경기도 안산시 단원구': '41273', '경기도 고양시': '41280', '경기도 고양시 덕양구': '41281', '경기도 고양시 일산동구': '41285', '경기도 고양시 일산서구': '41287', '경기도 과천시': '41290', '경기도 구리시': '41310', '경기도 남양주시': '41360', '경기도 오산시': '41370', '경기도 시흥시': '41390', '경기도 군포시': '41410', '경기도 의왕시': '41430', '경기도 하남시': '41450', '경기도 용인시': '41460', '경기도 용인시 처인구': '41461', '경기도 용인시 기흥구': '41463', '경기도 용인시 수지구': '41465', '경기도 파주시': '41480', '경기도 이천시': '41500', '경기도 안성시': '41550', '경기도 김포시': '41570', '경기도 화성시': '41590', '경기도 광주시': '41610', '경기도 양주시': '41630', '경기도 포천시': '41650', '경기도 여주시': '41670', '경기도 연천군': '41800', '경기도 가평군': '41820', '경기도 양평군': '41830', '충청북도': '43000', '충청북도 청주시': '43110', '충청북도 청주시 상당구': '43111', '충청북도 청주시 서원구': '43112', '충청북도 청주시 흥덕구': '43113', '충청북도 청주시 청원구': '43114', '충청북도 충주시': '43130', '충청북도 제천시': '43150', '충청북도 보은군': '43720', '충청북도 옥천군': '43730', '충청북도 영동군': '43740', '충청북도 증평군': '43745', '충청북도 진천군': '43750', '충청북도 괴산군': '43760', '충청북도 음성군': '43770', '충청북도 단양군': '43800', '충청남도': '44000', '충청남도 천안시': '44130', '충청남도 천안시 동남구': '44131', '충청남도 천안시 서북구': '44133', '충청남도 공주시': '44150', '충청남도 보령시': '44180', '충청남도 아산시': '44200', '충청남도 서산시': '44210', '충청남도 논산시': '44230', '충청남도 계룡시': '44250', '충청남도 당진시': '44270', '충청남도 금산군': '44710', '충청남도 부여군': '44760', '충청남도 서천군': '44770', '충청남도 청양군': '44790', '충청남도 홍성군': '44800', '충청남도 예산군': '44810', '충청남도 태안군': '44825', '전라남도': '46000', '전라남도 목포시': '46110', '전라남도 여수시': '46130', '전라남도 순천시': '46150', '전라남도 나주시': '46170', '전라남도 광양시': '46230', '전라남도 담양군': '46710', '전라남도 곡성군': '46720', '전라남도 구례군': '46730', '전라남도 고흥군': '46770', '전라남도 보성군': '46780', '전라남도 화순군': '46790', '전라남도 장흥군': '46800', '전라남도 강진군': '46810', '전라남도 해남군': '46820', '전라남도 영암군': '46830', '전라남도 무안군': '46840', '전라남도 함평군': '46860', '전라남도 영광군': '46870', '전라남도 장성군': '46880', '전라남도 완도군': '46890', '전라남도 진도군': '46900', '전라남도 신안군': '46910', '경상북도': '47000', '경상북도 포항시': '47110', '경상북도 포항시 남구': '47111', '경상북도 포항시 북구': '47113', '경상북도 경주시': '47130', '경상북도 김천시': '47150', '경상북도 안동시': '47170', '경상북도 구미시': '47190', '경상북도 영주시': '47210', '경상북도 영천시': '47230', '경상북도 상주시': '47250', '경상북도 문경시': '47280', '경상북도 경산시': '47290', '경상북도 의성군': '47730', '경상북도 청송군': '47750', '경상북도 영양군': '47760', '경상북도 영덕군': '47770', '경상북도 청도군': '47820', '경상북도 고령군': '47830', '경상북도 성주군': '47840', '경상북도 칠곡군': '47850', '경상북도 예천군': '47900', '경상북도 봉화군': '47920', '경상북도 울진군': '47930', '경상북도 울릉군': '47940', '경상남도': '48000', '경상남도 창원시': '48120', '경상남도 창원시 의창구': '48121', '경상남도 창원시 성산구': '48123', '경상남도 창원시 마산합포구': '48125', '경상남도 창원시 마산회원구': '48127', '경상남도 창원시 진해구': '48129', '경상남도 진주시': '48170', '경상남도 통영시': '48220', '경상남도 사천시': '48240', '경상남도 김해시': '48250', '경상남도 밀양시': '48270', '경상남도 거제시': '48310', '경상남도 양산시': '48330', '경상남도 의령군': '48720', '경상남도 함안군': '48730', '경상남도 창녕군': '48740', '경상남도 고성군': '48820', '경상남도 남해군': '48840', '경상남도 하동군': '48850', '경상남도 산청군': '48860', '경상남도 함양군': '48870', '경상남도 거창군': '48880', '경상남도 합천군': '48890', '제주특별자치도': '50000', '제주특별자치도 제주시': '50110', '제주특별자치도 서귀포시': '50130', '강원특별자치도': '51000', '강원특별자치도 춘천시': '51110', '강원특별자치도 원주시': '51130', '강원특별자치도 강릉시': '51150', '강원특별자치도 동해시': '51170', '강원특별자치도 태백시': '51190', '강원특별자치도 속초시': '51210', '강원특별자치도 삼척시': '51230', '강원특별자치도 홍천군': '51720', '강원특별자치도 횡성군': '51730', '강원특별자치도 영월군': '51750', '강원특별자치도 평창군': '51760', '강원특별자치도 정선군': '51770', '강원특별자치도 철원군': '51780', '강원특별자치도 화천군': '51790', '강원특별자치도 양구군': '51800', '강원특별자치도 인제군': '51810', '강원특별자치도 고성군': '51820', '강원특별자치도 양양군': '51830', '전북특별자치도': '52000', '전북특별자치도 전주시': '52110', '전북특별자치도 전주시 완산구': '52111', '전북특별자치도 전주시 덕진구': '52113', '전북특별자치도 군산시': '52130', '전북특별자치도 익산시': '52140', '전북특별자치도 정읍시': '52180', '전북특별자치도 남원시': '52190', '전북특별자치도 김제시': '52210', '전북특별자치도 완주군': '52710', '전북특별자치도 진안군': '52720', '전북특별자치도 무주군': '52730', '전북특별자치도 장수군': '52740', '전북특별자치도 임실군': '52750', '전북특별자치도 순창군': '52770', '전북특별자치도 고창군': '52790', '전북특별자치도 부안군': '52800'}
    result = dic_name[x]
    return result


def rprice():
    global df5            
    locs_name = combo51.get()+" "+combo52.get()
    loc = local_name(locs_name)
    locs=[]
    locs.append(loc)
    endm = datetime.datetime.today().strftime('%Y%m')
    startm = combo53.get()
    yms = period(startm[0:4]+startm[5:7], endm)
    
    #service_key = mymodule.key1()
    df_all = pd.DataFrame()
    
    urls = ["http://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade?LAWD_CD=",
            "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?LAWD_CD=",                    
            "http://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade?LAWD_CD=",
            "http://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade?LAWD_CD=",                    
            "http://apis.data.go.kr/1613000/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade?LAWD_CD=",
            "http://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent?LAWD_CD=",                    
            "http://apis.data.go.kr/1613000/RTMSDataSvcOffiRent/getRTMSDataSvcOffiRent?LAWD_CD=",
            "http://apis.data.go.kr/1613000/RTMSDataSvcRHRent/getRTMSDataSvcRHRent?LAWD_CD="]
    
    base_url = urls[rvar51.get()-1]
    
    col_eng=[
       ['umdNm','aptNm','excluUseAr','dealAmount','floor','jibun','dealDay','dealMonth','dealYear','dealingGbn','ownershipGbn','buyerGbn','slerGbn'],
       ['umdNm','aptNm','excluUseAr','dealAmount','buildYear','floor','dealDay','dealMonth','dealYear','dealingGbn','jibun','buyerGbn','slerGbn'],
       ['umdNm','offiNm','excluUseAr','dealAmount','buildYear','dealingGbn','floor','jibun','buyerGbn','slerGbn','dealDay','dealMonth','dealYear'],
       ['umdNm','mhouseNm','excluUseAr','dealAmount','jibun','buildYear','floor','houseType','landAr','dealingGbn','slerGbn','buyerGbn','dealDay','dealMonth','dealYear'],
       ['umdNm','jibun','landUse','plottageAr','buildingType','buildingUse','buildingAr','dealAmount','buildYear','dealingGbn','sggCd','slerGbn','floor','buyerGbn','dealDay','dealMonth','dealYear'],
       ['umdNm','aptNm','excluUseAr','deposit','monthlyRent','floor','jibun','buildYear','contractType','dealDay','dealMonth','dealYear'],
       ['umdNm','offiNm','excluUseAr','deposit','monthlyRent','floor','jibun','buildYear','dealDay','dealMonth','dealYear'],
       ['umdNm','mhouseNm','excluUseAr','deposit','monthlyRent','jibun','buildYear','floor','houseType','dealDay','dealMonth','dealYear']]
    
    col_kor=[
        ['읍면동','아파트명','전용면적','거래금액','층','지번','거래일','거래월','거래년','거래구분','분양입주권','매수자구분','매도자구분'],
        ['읍면동','아파트명','전용면적','거래금액','준공년도','층','거래일','거래월','거래년','거래구분','지번','매수자구분','매도자구분'],
        ['읍면동','오피스텔','전용면적','거래금액','준공년도','거래구분','층','지번','매수자구분','매도자구분','거래일','거래월','거래년'],
        ['읍면동','빌라','전용면적','거래금액','지번','준공년도','층','주택유형','대지권','거래구분','매도자구분','매수자구분','거래일','거래월','거래년'],
        ['읍면동','용도지역','대지면적','거래금액','빌딩유형','건물용도','연면적','지번','준공년도','거래구분','시군구코드','매수자구분','층','매도자구분','거래일','거래월','거래년'],
        ['읍면동','아파트명','전용면적','보증금','월세','층','지번','준공년도','계약유형','거래일','거래월','거래년'],
        ['읍면동','오피스텔','전용면적','보증금','월세','층','지번','준공년도','거래일','거래월','거래년'],
        ['읍면동','빌라','전용면적','보증금','월세','지번','준공년도','층','주택유형','거래일','거래월','거래년']]
    
    
    for ym in yms:
        for loc in locs:                    
            url = base_url + str(loc)+"&numOfRows=10000&DEAL_YMD="+str(ym)+"&serviceKey="+mykey
            res = requests.get(url)
            result = xmltodict.parse(res.content)
            try:
                data=result['response']['body']['items']['item']
                dfa=pd.DataFrame(data)                                        
                df_all = pd.concat([df_all, dfa])                                         
            except:
                pass
    df_all = df_all[col_eng[rvar51.get()-1]]
    df_all.columns = col_kor[rvar51.get()-1]
    df5=df_all.copy()
    clear_data()
    tv["column"] = list(df5.columns)
    tv["show"] = "headings"
    for column in tv["columns"]:
        tv.heading(column, text=column, anchor='w') # let the column heading = column name
        #.column(column, minwidth=0, width=180, stretch=NO) #no로 하면 전체화면에 맞추지 않음
        tv.column(column, minwidth=10, width=20, anchor='w') 
    tv.column("#4", minwidth=10, width=20, anchor='e') 
    tv.column("#5", minwidth=10, width=20, anchor='e') 
        #.column("층", width=80, anchor='center')
    #tv2.column("#6", width=50, anchor='e') #보이지 않는 칼럼인 id(0)을 제외한 칼럼번호
    df_rows = df5.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.thtml#tkinter.tTreeview.insert
    lab55.config(text='검색건수는 '+str(len(df5))+"건 입니다.")
    return None                                             
        
def save_as_file5():            
    try:
        #df5.to_excel(file_path, index=False)    
        df5.to_clipboard(index=False)
        msgbox.showinfo("알림", "Ctrl+C 복사하였습니다.")
    except:
        pass 
# =============================================================================
# def xls_down():
#     filename='result_'+ datetime.datetime.now().isoformat()[0:10] + '.xlsx'
#     df.to_excel(filename, index=False)    
#     msgbox.showinfo("알림", filename+"으로 다운로드 하였습니다.")
# =============================================================================

main_category=['서울특별시','경기도','인천광역시','부산광역시','대구광역시','대전광역시','광주광역시','울산광역시','세종특별자치시',\
        '강원특별자치도','충청북도','충청남도','전북특별자치도','전라남도','경상북도','경상남도','제주특별자치도']    



# 행정구는 제외해야 함.
gw_list=['강릉시','고성군','동해시','삼척시','속초시','양구군','양양군','영월군','원주시','인제군','정선군','철원군','춘천시','태백시','평창군','홍천군','화천군','횡성군']
gg_list=['가평군','고양시 덕양구','고양시 일산동구','고양시 일산서구','과천시','광명시','광주시','구리시','군포시','김포시','남양주시','동두천시','부천시 소사구','부천시 오정구','부천시 원미구','성남시 분당구','성남시 수정구','성남시 중원구','수원시 권선구','수원시 영통구','수원시 장안구','수원시 팔달구','시흥시','안산시 단원구','안산시 상록구','안성시','안양시 동안구','안양시 만안구','양주시','양평군','여주시','연천군','오산시','용인시 기흥구','용인시 수지구','용인시 처인구','의왕시','의정부시','이천시','파주시','평택시','포천시','하남시','화성시']
gn_list=['거제시','거창군','고성군','김해시','남해군','밀양시','사천시','산청군','양산시','의령군','진주시','창녕군','창원시 마산합포구','창원시 마산회원구','창원시 성산구','창원시 의창구','창원시 진해구','통영시','하동군','함안군','함양군','합천군']
gb_list=['경산시','경주시','고령군','구미시','김천시','문경시','봉화군','상주시','성주군','안동시','영덕군','영양군','영주시','영천시','예천군','울릉군','울진군','의성군','청도군','청송군','칠곡군','포항시 남구','포항시 북구']
gwangju_list=['광산구','남구','동구','북구','서구']
daegu_list=['군위군','남구','달서구','달성군','동구','북구','서구','수성구','중구']
daejon_list=['대덕구','동구','서구','유성구','중구']
busan_list=['강서구','금정구','기장군','남구','동구','동래구','부산진구','북구','사상구','사하구','서구','수영구','연제구','영도구','중구','해운대구']
seoul_list=['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구','노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구','성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']
sejong_list=['세종시']
ulsan_list=['남구','동구','북구','울주군','중구']
inchon_list=['강화군','계양구','남동구','동구','미추홀구','부평구','서구','연수구','옹진군','중구']
jn_list=['강진군','고흥군','곡성군','광양시','구례군','나주시','담양군','목포시','무안군','보성군','순천시','신안군','여수시','영광군','영암군','완도군','장성군','장흥군','진도군','함평군','해남군','화순군']
jb_list=['고창군','군산시','김제시','남원시','무주군','부안군','순창군','완주군','익산시','임실군','장수군','전주시 덕진구','전주시 완산구','정읍시','진안군']
jeju_list=['서귀포시','제주시']
cn_list=['계룡시','공주시','금산군','논산시','당진시','보령시','부여군','서산시','서천군','아산시','예산군','천안시 동남구','천안시 서북구','청양군','태안군','홍성군']
cb_list=['괴산군','단양군','보은군','영동군','옥천군','음성군','제천시','증평군','진천군','청주시 상당구','청주시 서원구','청주시 청원구','청주시 흥덕구','충주시']
  
def get_category5(eventObject): # eventObejct 자리에는 아무 값이나 들어가도 괜찮습니다.
    if combo51.get()=="서울특별시":
        combo52.config(value=seoul_list)                
        combo52.set("")
    elif combo51.get()=="경기도":
        combo52.config(value=gg_list)
        combo52.set("")
    elif combo51.get()=="인천광역시":
        combo52.config(value=inchon_list)
        combo52.set("")
    elif combo51.get()=="부산광역시":
        combo52.config(value=busan_list)
        combo52.set("")
    elif combo51.get()=="대전광역시":
        combo52.config(value=daejon_list)
        combo52.set("")
    elif combo51.get()=="대구광역시":
        combo52.config(value=daegu_list)
        combo52.set("")
    elif combo51.get()=="광주광역시":
        combo52.config(value=gwangju_list)
        combo52.set("")
    elif combo51.get()=="울산광역시":
        combo52.config(value=ulsan_list)
        combo52.set("")
    elif combo51.get()=="세종특별자치시":
        combo52.config(value=sejong_list)
        combo52.set("")
    elif combo51.get()=="강원특별자치도":
        combo52.config(value=gw_list)
        combo52.set("")
    elif combo51.get()=="충청북도":
        combo52.config(value=cb_list)
        combo52.set("")
    elif combo51.get()=="충청남도":
        combo52.config(value=cn_list)
        combo52.set("")
    elif combo51.get()=="전북특별자치도":
        combo52.config(value=jb_list)
        combo52.set("")
    elif combo51.get()=="전라남도":
        combo52.config(value=jn_list)
        combo52.set("")
    elif combo51.get()=="경상북도":
        combo52.config(value=gb_list)
        combo52.set("")
    elif combo51.get()=="경상남도":
        combo52.config(value=gn_list)
        combo52.set("")
    elif combo51.get()=="제주특별자치도":
        combo52.config(value=jeju_list)
        combo52.set("")
        
def clear_data():
    tv.delete(*tv.get_children())
    return None
        


###GUI#################################################################
###GUI#################################################################        
notebook = ttk.Notebook(root)  #tab
style = ttk.Style()
style.configure('TNotebook.Tab', font=('맑은고딕', 9))
style.map("TNotebook.Tab", foreground=[("selected", "red")])
notebook.pack()
        
###5. main_frame5
main_frm = Frame(notebook, width=1600, height=640)
main_frm.pack(fill='both', expand=1)        
    #LabelFrame for conditon        
lfrm = LabelFrame(main_frm, text="검색조건")        
lfrm.place(width=1600, height=140, rely=0.02, relx=0)
#radiobutton
rvar51 = IntVar()
rb51 = Radiobutton(lfrm, text='분양권', value=1, variable=rvar51)
rb51.invoke() #default value select
rb52 = Radiobutton(lfrm, text='아파트매매', value=2, variable=rvar51)
rb53 = Radiobutton(lfrm, text='오피스텔매매', value=3, variable=rvar51)
rb54 = Radiobutton(lfrm, text='빌라매매', value=4, variable=rvar51)
rb55 = Radiobutton(lfrm, text='상업용매매', value=5, variable=rvar51)             
rb56 = Radiobutton(lfrm, text='아파트전세', value=6, variable=rvar51)        
rb57 = Radiobutton(lfrm, text='오피스텔전세', value=7, variable=rvar51)
rb58 = Radiobutton(lfrm, text='빌라전세', value=8, variable=rvar51)

rb51.place(rely=0.1, relx=0)
rb52.place(rely=0.1, relx=0.08)
rb53.place(rely=0.1, relx=0.16)
rb54.place(rely=0.1, relx=0.24)
rb55.place(rely=0.1, relx=0.32)
rb56.place(rely=0.1, relx=0.40)
rb57.place(rely=0.1, relx=0.48)
rb58.place(rely=0.1, relx=0.56)        
    #Label
lab51 = Label(lfrm, text="광역시도")
lab51.place(rely=0.45, relx=0)
lab52 = Label(lfrm, text="시자치구")
lab52.place(rely=0.45, relx=0.15)
lab53 = Label(lfrm, text="기준월(>=)")
lab53.place(rely=0.45, relx=0.30)   
     
    #Combobox                     
combo51=ttk.Combobox(lfrm, height=len(main_category), value=main_category)                
combo51.place(rely=0.60, relx=0)
combo51.bind("<<ComboboxSelected>>", get_category5) # event, triggerd function

combo52 = ttk.Combobox(lfrm, values=[""])
combo52.set("")
combo52.place(rely=0.60, relx=0.15)

sdate = datetime.datetime.now() +  MonthEnd(-3)
edate = datetime.datetime.now() +  MonthEnd(0)
dates = pd.date_range(sdate, edate, freq="ME")
#dates =['2024-07-31','2024-08-31','2024-09-30']
values=[]
for i in dates:
    values.append(i.isoformat()[0:10])

combo53 = ttk.Combobox(lfrm, values=values)
combo53.place(rely=0.60, relx=0.30)
combo53.set(values[-4])

    #Button
button51 = Button(lfrm, text="검색실행", command=lambda: rprice())
button51.place(rely=0.60, relx=0.60)
#button2 = Button(file_frame, text="엑셀다운로드", command=lambda: xls_down())
button52 = Button(lfrm, text="Ctrl+C", width=20, command=lambda: save_as_file5())
button52.place(rely=0.60, relx=0.85)

#LabelFrame for TreeView
lfrm2 = LabelFrame(main_frm, text="조회결과")
lfrm2.place(width=1600, height=380, rely=0.28, relx=0)

#style = ttk.Style(lfrm2)
#style.theme_use("clam")
#style.configure("Treeview.Heading", background="green", foreground="white")

    #Treeview Widget
tv = ttk.Treeview(lfrm2)
tv.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly5 = Scrollbar(lfrm2, orient="vertical", command=tv.yview) 
treescrollx5 = Scrollbar(lfrm2, orient="horizontal", command=tv.xview) 
tv.configure(xscrollcommand=treescrollx5.set, yscrollcommand=treescrolly5.set)
treescrollx5.pack(side="bottom", fill="x") 
treescrolly5.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

#LabelFrame for result
lfrm3 = LabelFrame(main_frm, text="Result")
lfrm3.place(width=1600, height=80, rely=0.9, relx=0)

lab55 = Label(lfrm3, text="")
lab55.place(rely=0.2, relx=0)           

notebook.add(main_frm, text='실거래API')                        
        
root.mainloop()                        
