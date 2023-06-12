import re
re_ipv4 = r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
re_domain = r'((^|(?<=//))[\w\-\.]*\.[a-zA-Z]{2,6}(?=(:\d{1,5})|/|$))'
# re_domain = r'((^|(?<=//))[\w\-]*\.[\w\-\.]*[a-zA-Z](?=(:\d{1,5})|/|$))'
re_subdomain = r'[\w-]*\.\w*$'

ips,domains,subdomains = list(),list(),list()
fp = open("target.txt","r")
f = fp.read()
fp.close()
_list = f.split("\n")

for line in _list:
    ip=re.search(re_ipv4, line)
    if ip:
        ips.append(ip[0])

    domain=re.search(re_domain, line)
    if domain:
        domains.append(domain[0])
        subdomain = re.search(re_subdomain, domain[0])
        if(subdomain):
            subdomains.append(subdomain[0])

subdomains = set(subdomains)
ips = set(ips)
domains = set(domains)
# print(domains)
# print(ips)
# print(set(subdomains))

# print('======ip=====')
fp = open('ips.txt','w')
for ip in ips:
    fp.write(ip+'\n')
    print(ip)
fp.close()

print('======doamin=====')
fp = open('domains.txt','w')
for domain in domains:
    fp.write(domain+'\n')
    print(domain)
fp.close()

print('======subdoamin=====')
fp = open("subdomains.txt",'w')
for subdomain in subdomains:
    fp.write(subdomain+'\n')
    print(subdomain)
fp.close()


