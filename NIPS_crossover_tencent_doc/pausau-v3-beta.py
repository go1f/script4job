import requests
import bs4
import json
import re
import js2py
import time
import random


def tianmu_autologin():
    tianmu_url = 'http://cant-tell-you/'
    tianmu_login_url = tianmu_url + 'login/do_login'
    tianmu_session = dict()
    data = {
        "User" : "admin",
        "plain" : "can't-tell-you"
    }

    headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "close"
    }

    try:
        fp = open('encode.js')
        js_code = fp.read()
    except IOError:   
        print("需要加载encode.js, 请联系高队长获取。")
        exit()
    finally:
        fp.close()

    context = js2py.EvalJs()
    context.execute(js_code)
    time_passwd = str(context.hash(data["User"],data["plain"]))
    time_passwd = time_passwd.replace("'","\"")

    data = {**data,**(json.loads(time_passwd))}
    post_data = dict({'data': data})
    post_data = json.dumps(post_data)
    # print(post_data)

    rep = requests.post(url=tianmu_login_url, data=post_data, headers = headers)
    result = str(rep.text)

    if(result.find('"login":0')!=-1):
        tianmu_session['PHPSESSID'] = str(rep.cookies['PHPSESSID'])
        print("Tianmu auto login success!!!")
    else:
        print("未知原因，天幕登录失败。")
        #如手动添加了token，可忽略此告警。

    rep = requests.get(url=tianmu_url, cookies=tianmu_session, data=post_data, headers=headers)

    # print(re.findall(r"userToken: \"(.+?)\",",str(rep.text)))
    tianmu_session['token'] = re.findall(r"userToken: \"(.+?)\",", str(rep.text))[0]

    # print(tianmu_session)
    return(tianmu_session)

def get_history_ip():
    history_list = []
    try:
        fp = open('history_ip.txt','r')
        for line in fp:
            line = line.strip().replace('\n','').replace('\r','').replace(' ','')
            history_list.append(line)
    finally:
        fp.close()
        # print('get_history_ips')
        # print(history_list)
    return set(history_list)

def save_files(_set):
    try:
        fp = open('history_ip.txt','a')
        for line in _set[0]:
            fp.write(str(line)+'\n')
    finally:
        fp.close()


    try:    
        f = open('white_ip.txt','a')
        for ip in _set[1]:
            f.write(str(ip)+'\n')
    finally:
        fp.close()

def get_onduty_ip():
    onduty_list = []
    # Use a breakpoint in the code line below to debug your script.
    url = "https://docs.qq.com/sheet/can't-tell-you"
    url_extra = "https://docs.qq.com/dop-api/get/sheet?tab=can't-tell-you&wb=1 "
    params = {
        'tab': 'BB08J2'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Cookie': "can't-tell-you"
    }
    headers_extra = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'X-Seq-Id': 'X-Seq-Id',
        'Connection': 'close',
        'referer': 'https://docs.qq.com/sheet/cant-tell-you',
        'Cookie': "can't-tell-you",

    }
    while True:
        try:
            r = requests.get(url, headers=headers, timeout=10, params=params)
            break
        except requests.exceptions.ConnectionError as e:
            # if(str(e).find('[WinError 10061]') != -1):
            print('网络问题, 正在等待重拨... ...')
            time.sleep(60)


    # print(r.content)
    html_content = r.content
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    # elems = example_soup.select('.s2')
    # print(elems)
    for idx, tr in enumerate(soup.find_all('tr')):
        if 1 < idx < 62:
            td = tr.find('td')
            span = td.find('span')
            if span is None:
                break
            ip = span.contents[0]
            ip.strip().replace('\n','').replace('\r','').replace(' ','')
            onduty_list.append(ip)
        if idx > 61:
            r = requests.get(url_extra, headers=headers_extra)
            pattern = re.compile(
                r'((?:(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d))\.){3}(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d)))')
            ip_info = pattern.findall(r.text)
            for i in ip_info:
                i.strip().replace('\n','').replace('\r','').replace(' ','')
                onduty_list.append(i)
            break
    # print(onduty_list)

    return set(onduty_list)


def block_request(ip):
    # print(type(session['PHPSESSID']))
    # print(type(session['token']))
    tianmu_url = 'http://cant-tell-you/'
    tianmu_url = tianmu_url + 'api?i=psg/GlobalAccessInterfaceIAddRule'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'close',
    }
    ip_data = {"src_ip": ip, "dst_ip": ""}
    ip_data_list = [ip_data]
    tianmu_json_data = {
        "serviceType": "psg",
        "action": "GlobalAccessInterfaceIAddRule",
        "region": "",
        "data": {
            "Type": "BLACK",
            "Id": "",
            "Name": "test",
            "ValidDuration": -1,
            "MatchOperation": "1",
            "SourcePlatform": "天幕平台",
            "IsOverwrite": "1",
            "IpType": "source",
            "IpData": json.dumps(ip_data_list),
            "RegionId": "region1",
            "Az": [""],
            "Version": "2018-12-10",
            "Region": ""
        },
        "userToken": session['token']
    }
    tianmu_json_data['data']['Name'] = 'psg_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_' + ip
    res = requests.post(tianmu_url, cookies=session, data=json.dumps(tianmu_json_data), headers=headers)

    
    return str(res.text)
    


def block(_set):
    private = r'^(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|(172\.((1[7-9])|(2\d)|(3[01]))\.\d{1,3}\.\d{1,3})|(192\.168\.\d{1,3}\.\d{1,3})$'
    ipv4 = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'

    white_list = []
    newadd_list = []

    for ip in _set:
        # 过滤错误IPV4格式或内网IP的字符串
        if not re.match(ipv4,ip):
            continue
        if re.findall(private, ip):
            print(ip, ' 内网ip!!!已拒绝添加!!!')
            continue
        
        # 发送加黑请求
        result = block_request(ip)
        
        if(result.find('\\u89c4\\u5219\\u51b2\\u7a81')!=-1):
            print(str(ip)+" 已存在黑名单中!!!")

        elif(result.find('redirect')!=-1):
            print("天幕Token过期!!!请重新运行脚本即可!!!")
            exit()

        elif(result.find('\\u8be5IP\\u5df2\\u5b58\\u5728\\u767d\\u540d\\u5355\\u4e2d')!=-1):
            print(str(ip)+" 与白名单冲突 !!!!!!!!!!!")
            white_list.append(ip)

        elif(result.find('"warning_rule":[]')!=-1):
            print(ip, ' 封禁成功。')
            # print(txt)
        else:
            print(ip)
            print(result)

        newadd_list.append(ip) # 有可能黑白名单冲突
        
    return newadd_list,white_list

def tianmu_block():
    onduty_set = get_onduty_ip()
    history_set = get_history_ip()
    filter_set = set(onduty_set) - set(history_set)

    _set_tumple = block(filter_set)
    save_files(_set_tumple)


def wait_a_second(seconds):
    bye_list = ['Sa yo ra la', 'zZZ......', 'One more round! ', 'Catch you later. ', '3Beta版本不保证稳定性, 请联系邓经理提交issues ', '若有新需求, 请联系邓经理 ', '今天OUT了没? ', '今天打卡了吗? ', '今天签到了没? ', '快九点了没?', '欢迎试用扒手III beta! ', '下一波殭尸30秒到达!!','大吉大利!!没有IP!! ', '不闹。' , '寇队员请开展摸鱼排查!! ', '久坐有害健康!! ', 'Paasau 3全新改版: 天幕自动登录。']
    luck_num = random.randint(0,len(bye_list)-1)
    print(bye_list[luck_num] + '\n\n')

    time.sleep(seconds)


title = '''
   .-..     .---.    .---.        .--.      .---.   ___  ___   
  /    \\   / .-, \\  / .-, \\     /  _  \\    / .-, \\ (   )(   ) 
 ' .-,  ; (__) ; | (__) ; |    . .' `. ;  (__) ; |  | |  | |   
 | |  . |   .'`  |   .'`  |    | '   | |    .'`  |  | |  | |    
 | |  | |  / .'| |  / .'| |    _\\_`. (__)  / .'| |  | |  | | 
 | |  | | | /  | | | /  | |   (   ). '.   | /  | |  | |  | |  
 | |  ' | ; |  ; | ; |  ; |    | |  `\\ |  ; |  ; |  | |  ; ' 
 | `-'  ' ' `-'  | ' `-'  |    ; '._,' '  ' `-'  |  ' `-'  /  
 | \\__.'  `.__.'_. `.__.'_.     '.___.'   `.__.'_.   '.__.'  
 | |                                                                      
(___)                                                              
'''
if __name__ == '__main__':

    print(title)
    session = tianmu_autologin()
    while True:
        timing = str(time.strftime('%m-%d %H:%M:%S')).join(['---- ',' -----'])
        print(timing)

        tianmu_block()

        wait_a_second(30)

