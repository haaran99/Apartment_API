from typing import Counter
import requests
from xml.etree.ElementTree import Element, dump
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
import pymysql
import re

######################Mysql 접속####################################
db_conn = pymysql.connect(
        host='아이피', 
        port=3306, 
        user='root', 
        passwd='비밀번호', 
        db='gyeonggido', 
        charset='utf8')
######################Mysql 커리 날리기####################################

curs = db_conn.cursor()

######################데이터 받기###########################################
year = 2010
while year <= 2021:
    print(year)
    year += 1
    mon = 1
    while mon <= 12:
        mon = format(mon, '02')
        url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
        LAWD_CD = '41173'
        DEAL_YMD = str(year)+str(mon)
        print(DEAL_YMD+"년도")
        servicekey = '키값'
        (str(servicekey))
        
        queryParams = '?LAWD_CD=' + LAWD_CD + '&DEAL_YMD=' + DEAL_YMD + '&serviceKey=' + servicekey

        res = requests.get(url + queryParams)
        mon = int(mon)
        mon = mon + 1
        ######################데이타 정리 ####################################
        def get_items(res):
            root = ET.fromstring(res.content)
            item_list = []
            for child in root.find('body').find('items'):
                elements = child.findall('*')
                data = {}
                for element in elements:
                    tag = element.tag.strip()
                    text = element.text.strip()
                    # print tag, text
                    data[tag] = text
                item_list.append(data)  
            return item_list

        list_data = get_items(res)
        ######################################################################

        #print(list_data) ## 데이터 확인

        i=0
        while i <= len(list_data):
            list_data = get_items(res)[i]
            YEAR = list_data["년"]
            MONTH = list_data["월"]
            DAY = list_data["일"]
            LOCAL_DONG = list_data["법정동"]
            APARTMENT = list_data["아파트"]
            LAYER = list_data["층"]
            COST = list_data["거래금액"]
            COST = COST.replace(",","")
            CRATE_YEAR = list_data["건축년도"]
            LOCAL_CODE = list_data["지역코드"]
            AREA = list_data["전용면적"]
            PYUNG = round(float(AREA)/3.3,1)
            DATA = (YEAR,MONTH,DAY,LOCAL_DONG,APARTMENT,LAYER,COST,CRATE_YEAR,LOCAL_CODE,AREA,PYUNG)
            print(DATA)
            sql = 'insert into anyang (YEAR,MONTH,DAY,LOCAL_DONG,APARTMENT,LAYER,COST,CRATE_YEAR,LOCAL_CODE,AREA,PYUNG) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            curs.execute(sql,DATA)
            db_conn.commit()
            i+=1
