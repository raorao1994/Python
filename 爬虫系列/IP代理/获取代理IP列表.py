# 仅爬取西刺代理首页IP地址

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request

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


if __name__ == '__main__':
    url = 'http://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')     # 解析获取到的html
    get_ip_list(bsObj)