from re import search
from os import path as ospath, mkdir

input_filename = "input.txt"

if not ospath.exists(input_filename):
    print(f"未找到输入文件{input_filename}")
    input()
    exit(1)

re_ipv4 = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
re_domain = r"((^|(?<=//))[\w\-\.]*\.[a-zA-Z]{2,6}(?=(:\d{1,5})|/|$))"
ips, index_domains, domains = list(), list(), list()

with open(input_filename, "r") as r:
    lines = r.readlines()

# 特殊二级域名，如com.cn，org.cn，需要补充一下
special_domain = ["com", "org", "gov"]

for line in lines:
    # 去掉换行符
    line = line.replace("\n", "")
    # 搜索ipv4地址
    ip = search(re_ipv4, line)
    if ip:
        ips.append(ip[0] + "\n")
        continue

    # 域名（包括子域名）
    _domain = search(re_domain, line)
    if _domain:
        domains.append(_domain[0] + "\n")
        domain = _domain[0]
        # 提取主域名
        _t = domain.split(".")
        if _t[-2] in special_domain:
            domain = _t[-3] + "." + _t[-2] + "." + _t[-1]
        else:
            domain = _t[-2] + "." + _t[-1]
        index_domains.append(domain + "\n")


if not ospath.exists("result"):
    mkdir("result")

with open("result/ips.txt", "w") as w:
    w.writelines(set(ips))

with open("result/domains.txt", "w") as w:
    w.writelines(set(domains))

with open("result/index_domains.txt", "w") as w:
    w.writelines(set(index_domains))

print("结果已输入指result文件夹")
