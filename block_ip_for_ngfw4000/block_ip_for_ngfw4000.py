import requests
import ipaddr
import glob
import re

def get_onfile_ip():
	blocked_ip = set()
	blocked_subnet = set()

	for file in glob.glob('ip/*.txt'):
	    f = open(file, 'r', encoding='utf-8')
	    for line in f:
	        line = line.strip().replace('\n','').replace('\r','').replace(' ','')
	        if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',line):
	            blocked_ip.add(line)
	        elif re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/\d{1,2}$',line):
	        	blocked_subnet.add(line)
	    f.close()

	str1 = '\n'.join(blocked_ip)
	f = open("blocked_ip.txt","w")
	f.write(str1)
	f.close()

	str2 = '\n'.join(blocked_subnet)
	f = open("blocked_subnet.txt","w")
	f.write(str2)
	f.close()

	return blocked_ip,blocked_subnet

def get_fresh_ip(ip_filename, blocked_ip_subnet):
	blocked_ip = blocked_ip_subnet[0]
	blocked_subnet = blocked_ip_subnet[1]

	fresh_subnet = set()
	fresh_ip = set()

	fp = open(ip_filename,'r')
	for line in fp:
	    line = line.strip().replace('\n','').replace('\r','').replace(' ','')
	    if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',line) and line not in blocked_ip:
	        fresh_ip.add(line)
	    elif re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/\d{1,2}$',line) and line not in blocked_subnet:
	    	fresh_subnet.add(line)
	fp.close()

	print('黑名单将新增 '+str(len(fresh_ip))+'个IP 和 '+str(len(fresh_subnet))+'个网段')
	print('目前已封禁 '+str(len(blocked_ip)+len(fresh_ip))+'个IP 与 '+str(len(blocked_subnet)+len(fresh_subnet))+'个网段')
	fresh_ip = list(fresh_ip)
	fresh_ip.sort()	
	return fresh_ip,fresh_subnet

def edit_hostgroup(group_name, ip_list):
	data = 'def_host_name='+ group_name +'&def_host_mac=00%3A00%3A00%3A00%3A00%3A00&host_ipad_input=&name_hidden='+ group_name +'&def_host_frompage=&def_host_from=&def_host_edt_but=+%C8%B7%B6%A8+'
	data += '&def_host_ipad='.join(ip_list)

	url="https://"+host+"/cgi/maincgi.cgi?Url=HostObj&Act=Edit&Name=" + group_name
	req = requests.post(url=url, data=data, verify=False, headers=headers,cookies=cookie)
	
	if req.content.decode('gbk').find("alert(\"error -")==-1 :
		print('请忽略SSL-Warning.\nOK!')
	else:
		print('存在错误！')
		print(req.content.decode("gbk"))

def group_exist(name):
	url = "https://"+host+"/cgi/maincgi.cgi?Url=Ajax&Act=IsNameExist&Name="+name
	req = requests.get(url=url, cookies=cookie, headers=headers, verify=False)
	if req.content == b'EXIST':
		return True
	else:
		return False

def create_hostgroup(name):
	data = "def_host_mac=00%3A00%3A00%3A00%3A00%3A00&def_host_add_but=+%C8%B7%B6%A8+&def_host_name="+name
	url = "https://"+ host +"/cgi/maincgi.cgi?Url=HostObj&Act=Edit"

	requests.post(url=url,data=data,verify=False,cookies=cookie,headers=headers)

def create_subnet(subnets):
	url="https://"+ host +"/cgi/maincgi.cgi?Url=SubnObj&Act=Add"
	for subnet in subnets:
		subnet = ipaddr.IPv4Network(subnet)
		data="nameTex=black-"+str(subnet)+"&ipTex="+str(subnet[0])+"&maskTex="+str(subnet.netmask)+"&def_subn_add_but=+%C8%B7%B6%A8+"
		req = requests.post(url=url, data=data, cookies=cookie, verify=False, headers=headers)


#将已封ip的txt文本放到目录下ip文件夹
#将将要封IP的txt文本放到同目录下
ip_filename = "blacklist-18.txt"
#每隔约1小时自行浏览器F12，复制粘贴更新Cookie
cookie={"session_id_443":"MTEyODA3MTQ5OTc1NDA="}
#填写当天日期
date_of_today= '15'
#NGFW所在地址
host='192.168.1.1'

headers = {
	"Host": host,
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
	"Content-Type": "application/x-www-form-urlencoded"
}

blocked_ip_subnet = get_onfile_ip()
blacklist = get_fresh_ip(ip_filename, blocked_ip_subnet)
ip_list = blacklist[0]
subnets = blacklist[1]

group_number = 0
num = 255 #单个主机组仅容纳255个IP
for i in range(0,len(ip_list),num):
	ip_list_chunk = ip_list[i:i+num]
	group_number += 1 
	ip_groupname = "blacklist-" + date_of_today + "-" + str(group_number)

	if group_exist(ip_groupname) == False:
		create_hostgroup(ip_groupname)

	edit_hostgroup(ip_groupname,ip_list_chunk)

create_subnet(subnets)