#encoding=utf8
import re
_ips = []

fp = open('ip/new_list.txt','r')
for line in fp:
    line = line.strip().replace('\n','').replace('\r','').replace(' ','')
    _ips.append(line)
fp.close()

_ips2 = []
fp = open('ip/blocked_ip.txt','r')
for line in fp:
    line = line.strip().replace('\n','').replace('\r','').replace(' ','')
    _ips2.append(line)
fp.close()

ipv4 = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
private = r'^(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|(172\.((1[7-9])|(2\d)|(3[01]))\.\d{1,3}\.\d{1,3})|(192\.168\.\d{1,3}\.\d{1,3})$'

bye_list = ['Goodbye next time. ','In seconds!','Comback soon. ','Farewell. ','Have a good day! ','Bye bye! ','Later! ','Catch you later. ','I\'m out! ','Next turn! ' ]

print(bye_list[2])

# print(set(_ips)-set(_ips2))

for ip in _ips:
    # 判断IP格式
    if re.match(ipv4,ip):
        # 判断内网IP
        if re.findall(private,ip):  
            print(str(ip))        
        else:
            
            continue  
