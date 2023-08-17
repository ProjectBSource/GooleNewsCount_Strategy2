import json
from urllib.request import urlopen
from datetime import datetime
import requests
import sys
import logging
import mysql.connector
import threading
import time


inserted_data = []
stock_list = {}
val = []

def lambda_handler(event, context):
    get_the_stocks()
    
    get_the_today_inserted_data()
    
    search_the_google_news()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def get_the_stocks():
    page_control = 1
    already_get_all = False
    while already_get_all==False:
        url = "https://finviz.com/screener.ashx?v=111&f=cap_large,sh_curvol_o5000&ft=4&o=-volume&r="+str(page_control)
        print(url)
        headers = {
            "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        splited_result = requests.get(url, headers=headers).text.split('</td></tr><!-- TS')
        for x in splited_result[1].split('TE -->')[0].split('\n'):
            if(len(x.strip())>0):
                symbol = x.split("|")[0]
                price = x.split("|")[1]
                volumn = x.split("|")[2]
                if((symbol in stock_list) == False):
                    stock_list[symbol]= [float(price), int(volumn)]
                else:
                    already_get_all = True
                    break
        page_control += 20
    print("stock_list size:",len(stock_list))
        

def get_the_today_inserted_data():
    #Get the inserted data today
    mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
    mycursor = mydb.cursor()
    sql = " SELECT Symbol, resultcount FROM patrick_strategy_1 WHERE DATE_FORMAT(CheckDate,'%Y%m%d') = DATE_FORMAT(NOW(),'%Y%m%d') "
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for data in result:
        inserted_data.append(data[0])
        

def search_the_google_news():
    url = "https://www.google.com/"
    session = requests.Session()
    response = session.get(url)
    temp_cookies = "AEC="+session.cookies.get_dict()['AEC']+"; NID="+session.cookies.get_dict()['NID']+"; 1P_JAR="+ (session.cookies.get_dict()['1P_JAR'])
    temp_cookies = "AEC=AUEFqZf5QkGw_Fu3sPTZ5LSzcBRo1Uin5IpiX8ZNoe0fBm8D0mHJJBD; NID=511=SFUnXI1jrlvUD2XG5AIkAZ9HcR92HKQ4gbW3kqZalTZvKINdy4vpvL_edKND6K4pvuMLbejywWtrvhyD0K6VasEg-DC4W6BawSHHp9cBQ3zpW4PhxRzuY9SbcoO7AdDAIiAkzteSdktWMYuD7Ubu87qu7CrIbWwW0LMPacd2brOQny9ODE7n8yrmvs6Tsp_xE8pQcXzUQ71eOcmsiVD_xFGbJ2aFtEYKV1n2joJo1Bo0N2Q6Ykf7J2ciEysQkEIKsg_pnEYvjvwXM8cpHTw-r3i95QPeoOZ-_X9SB5ygE2uU3kyotrfwHpD7sm58xcpfDpIlHsRlQGKR4JXicQ; 1P_JAR=2023-04-06-02"
    print('temp_cookies:' + temp_cookies)
    for x in stock_list:
        if((x in inserted_data)==True): 
            print(x , " already inserted")
        if((x in inserted_data)==False): 
            result_count = 0
            page_control = 0
            temp_page_count = 11;
            while temp_page_count == 11:
                url = "https://www.google.com/search?q="+x+".us&source=lnt&tbs=qdr:d&start="+str(page_control)
                headers = {
                    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                    "cookie": temp_cookies
                    #"cookie": 'OTZ=6668037_24_24__24_; SID=OAjIt6WjdSO15TTs8u9wxdJ06klHpwjIa9D4yZuI9RFMztGgjJ7UnQc_EdGMmnNJ0SWgRg.; __Secure-1PSID=OAjIt6WjdSO15TTs8u9wxdJ06klHpwjIa9D4yZuI9RFMztGgx0L3Q-5z37rGxVu8uTrDPg.; __Secure-3PSID=OAjIt6WjdSO15TTs8u9wxdJ06klHpwjIa9D4yZuI9RFMztGgoVv6r2Vsj7n5xd4vl54rQw.; HSID=AI2ZBs4WOEtXUG62u; SSID=Al6qMzJMvurPODBn9; APISID=Kd60rgkyedbOmOHu/A1qbek7qPUxod411S; SAPISID=lskkWidG8KibTvXj/AtxtFJxQPUNgC4vnv; __Secure-1PAPISID=lskkWidG8KibTvXj/AtxtFJxQPUNgC4vnv; __Secure-3PAPISID=lskkWidG8KibTvXj/AtxtFJxQPUNgC4vnv; 1P_JAR=2022-09-08-16; AEC=AakniGMynTwbXOMBoTaGLRdJd400cHyX7Tgw04f7T4J-gIyVMGJNwL3u9Q; NID=511=WNkDr1R37tyVl8Ua9y9RQgyCRiaYEAQ6iWu1itgYrhyoieob3BlofOKwPqJHiDMfAdLd4DjFgzKUnsYQdr-gKJK7JXsYczLU0OWs7E9vTgrDdJyJkGa1VLC8Co2MftGaflPAUrpUo0-criFZHVv77KVL0aVBPlL-_HuTlapApOYADE5Ohn_3xTETIkFaH_VMoOO_7eOth3FvS823LUV4gdqEGEloOILZPYDCy2soakT6RW_U7aVcNsdtDZfBePJIoo45npsT_0GSOJdERoF05b-8br47S8n2dIFn-r276J96W7kBFkJX2jyhMDIzdvc-Jw; DV=07zcPerMfJERYPXf0FOdhZDnKVXeMRg; SIDCC=AEf-XMQCsviGTzcW4xatJXItXFQBYE1ctAywgk8w100Tm2O8_A5PWTYDxUSiD-gpu_uqHFq9ew; __Secure-1PSIDCC=AEf-XMSapyc47hlJ59rcGNZ4rViWPztxsd3jkBve3fh740m-U68WbSXiTLMKk3EkUrBy_SCqfQ; __Secure-3PSIDCC=AEf-XMQvtKgPwn1sfDKXEub3VSauQuS6dhwDRnBJCEz25vSlFjefXENXaZxoQlJexCzBjJ1cQg'
                }
                response = requests.get(url, headers=headers)
                temp_page_count = len(response.text.split('data-snhf="0"'))
                if temp_page_count>1:
                    result_count += temp_page_count - 1
                page_control += 10
            if(result_count==0): break
            print("There is ", result_count, " results of ", x, ", price:", str(stock_list[x][0]), ", volumn:", str(stock_list[x][1]))
            val.append( ( x, str(result_count), str(stock_list[x][0]), str(stock_list[x][1]) ) )
    mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
    mycursor = mydb.cursor()
    sql = "INSERT INTO patrick_strategy_1 (CheckDate, Symbol, ResultCount, close, volumn) VALUES (NOW(), %s, %s, %s, %s) "
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
