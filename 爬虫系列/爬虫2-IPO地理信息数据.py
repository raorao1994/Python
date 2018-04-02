#encoding=utf-8
from bs4 import BeautifulSoup
import requests,sys
import os;
import time

#创建类
class DownLoad(object):
    #初始化
    def __init__(self):
        self.HTML="http://www.poi86.com/";#数据地址
        self.target="";#下载连接
        self.Provices={};
        self.Citys = {};
        self.Countys={};
        self.urls=[];#保存连接
    #获取所有省份
    def GetAllProvinces(self):
        url=self.HTML+"poi/amap.html";
        html=self.downLoadHtml(url=url);
        bf = BeautifulSoup(html)
        divs = bf.find_all('div', class_='col-md-2')
        fileText = open("MapPOI/全国省份信息.txt", "w+");
        for elemetnt in divs:
            provinceName=elemetnt.find_all('strong')[0].text;
            provinceUrl=elemetnt.find_all('a')[0]['href'];
            #print(provinceName);
            #print(provinceUrl);
            fileText.writelines(provinceName+","+provinceUrl+"\n")
            self.Provices[provinceName] = provinceUrl;
        fileText.flush()
        #fileText.closed();
        print("获取省份信息完成！！！")

    # 获取省份下的地级市
    def GetAllCity(self,url,name):
        url = self.HTML + url;
        html = self.downLoadHtml(url=url);
        bf = BeautifulSoup(html)
        divs = bf.find_all('li', class_='list-group-item')
        fileText = open("MapPOI/"+name+"城市信息.txt", "w+");
        #清空城市信息
        self.Citys.clear();
        for elemetnt in divs:
            cityName = elemetnt.find_all('a')[0].text;
            cityUrl = elemetnt.find_all('a')[0]['href'];
            fileText.writelines(cityName + "," + cityUrl + "\n")
            self.Citys[cityName] = cityUrl;
        fileText.flush()
        # fileText.closed();
        print("获取"+name+"城市信息完成！！！")

    #获取城市区县数据
    def GetAllCounty(self,url,name):
        url = self.HTML + url;
        html = self.downLoadHtml(url=url);
        bf = BeautifulSoup(html)
        divs = bf.find_all('li', class_='list-group-item')
        # 清空城市信息
        self.Countys.clear();
        for elemetnt in divs:
            countyName = elemetnt.find_all('a')[0].text;
            countyUrl = elemetnt.find_all('a')[0]['href'];
            self.Countys[countyName] = countyUrl;
        print("获取" + name + "城市信息完成！！！")

    #获取区县数据
    def GetDataByCounty(self,url,fileName):
        index = 1;
        url2 = url.split("/");
        url2 = htmlEngine.HTML + url2[1] + "/" + url2[2] + "/" + url2[3] + "/" + url2[4] + "/" + str(index) + ".html";
        file=open(fileName,"a");
        while index > 0:
            # 获取页面
            html = htmlEngine.downLoadHtml(url=url2);
            bf = BeautifulSoup(html)
            divs = bf.select("td a")
            for elemetnt in divs:
                #获取poi url地址
                href = elemetnt['href'];
                url3=self.HTML+href;
                html1=self.downLoadHtml(url3);
                bf1=BeautifulSoup(html1);
                spans = bf1.find_all("li", class_='list-group-item')
                title = bf1.find_all("h1");
                data = title[0].text + "," + spans[3].text + "," + spans[4].text + "," + spans[5].text + ",";
                data = data + spans[6].text + "," + spans[7].text + "," + spans[8].text + "\n";
                file.writelines(data);
                time.sleep(3)  # 休眠0.2秒
            index=index+1;
            file.flush();
            print(fileName+"文件添加数据："+str(index))
    #获取url连接html内容
    def downLoadHtml(self,url):
        request=requests.get(url=url);
        html=request.text;
        return html;

if __name__=="__main__":
    htmlEngine=DownLoad();
    #获取所有省份信息
    htmlEngine.GetAllProvinces();
    #获取省份下的地级市
    for pro in htmlEngine.Provices:
        #获取所有省份下的城市信息
        url=htmlEngine.Provices[pro];
        htmlEngine.GetAllCity(url=url,name=pro);
        #根据城市信息获取区县信息
        for city in htmlEngine.Citys:
            curl = htmlEngine.Citys[city];
            htmlEngine.GetAllCounty(url=curl,name=city);
            #循环打开区县
            for County in htmlEngine.Countys:
                print("开始下载"+County+"数据")
                url2=htmlEngine.Countys[County];
                file="MapPOI/data/"+pro+"数据.txt";
                htmlEngine.GetDataByCounty(url=url2,fileName=file)
                print("结束下载" + County + "数据")
        #休眠2秒
        time.sleep(3)#休眠3秒
    print("完成");