# 仅爬取西刺代理首页IP地址

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import socket
import urllib

#获取ip列表
def get_ip_list(obj):
    table=obj.findAll('table', {'id': 'ip_list'}) [0]  # 获取带有IP地址的表格的所有行
    ip_text = table.findAll('tr')   # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')
        if (len(ip_tag)>3):
            ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
            ip_list.append(ip_port)
    print("共收集到了{}个代理IP".format(len(ip_list)))
    print(ip_list)
    return ip_list

#获取随机代理
def get_random_ip(ip_list):
    import random
    random_ip = 'http://' + random.choice(ip_list)
    proxy_ip = {'http:': random_ip}
    return proxy_ip

#获取网页内容函数
def getHTMLText(url,proxies):
    try:
        r = request.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text;


#验证获得的代理IP地址是否可用
def validateIp(proxy):
    url = "http://ip.chinaz.com/getip.aspx"
    f = open("E:\ip.txt","w")
    socket.setdefaulttimeout(3)
    for i in range(0,len(proxy)):
        try:
            ip = proxy[i].strip().split(":")
            proxy_host = "http://"+ip[0]+":"+ip[1]
            proxy_temp = {"http":proxy_host}
            res = urllib.urlopen(url,proxies=proxy_temp).read()
            f.write(proxy[i]+'\n')
            print(proxy[i])
        except Exception :
            continue;
    f.close()

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')     # 解析获取到的html
    proxylist=get_ip_list(bsObj)
    validateIp(proxylist)