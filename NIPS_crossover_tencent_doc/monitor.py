#coding=utf8
import requests
import time
def mon():
    url = "https://huawei.fsgucun.com"
    # url = "https://www.baidu.com"
    header={
    "Host":"huawei.fsgucun.com",
    "Connection":"close",
    "Cache-Control":"max-age=0",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like ,Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/,webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site":"none",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-User":"?1",
    "Sec-Fetch-Dest":"document",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9"
    }

    try:
        html = requests.get(url, timeout=10).text
        print('Success !!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except requests.exceptions.RequestException as e:
        # if(str(e).find('[WinError 10061]') != -1):
        print('无法连接。')

while True:
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    mon()
    time.sleep(10)
