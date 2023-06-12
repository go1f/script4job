#!/bin/python3
# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom

def load_nmap_xml():
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("scanb.xml")
    if DOMTree.getElementsByTagName("host"):
        hosts = DOMTree.getElementsByTagName("host") 
    host_list = list()
    for host in hosts:
        address = host.getElementsByTagName("address")[0].getAttribute("addr")
        # print(address)
        ports = host.getElementsByTagName("port")
        port_list = list()
        for port in ports:
            if("open" == port.getElementsByTagName('state')[0].getAttribute("state")):
                port_value = port.getAttribute("portid")
                # print(port_value)
                port_list.append(port_value)
        if(port_list):
            host_list.append({"ip":address, "port_list":port_list})    
    # print(host_list)
    return host_list

port_checklist = ("22","139","53","111","ssh","135","445","samba","mysql","3306","1521","3389","21")
host_list = load_nmap_xml()
for host in host_list:
    for port in host["port_list"]:
        if(port in port_checklist):
            continue
        url = "http://%s:%s" %(host["ip"],port)
        # url = "http://"+str(host["ip"])+":"+str(port)
        print(url)