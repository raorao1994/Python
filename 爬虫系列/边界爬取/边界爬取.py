# -*- coding: utf-8 -*-
"""
Created on Sat May 19 07:59:29 2018

@author: Administrator
"""

import os;
import json;
import requests,sys

class DataDispose:
    #初始化数据
    def __init__(self):
        #类型code
        self.TypeCode="120000";
        #读取文件路径
        self.FilePathStr="D:/BaiduNetdiskDownload/整理/";
        #保存文件路径
        self.SaveDir="F:/GIS数据/整理/";
        #省份信息
        self.Province="北京市";
        #获取建筑物ID URL https://gaode.com/service/poiTipslite?geoobj=116.298521,39.949916&words=某某小区
        self.BuildUrl="https://gaode.com/service/poiTipslite?geoobj=";
        #获取建筑物边界URl https://www.amap.com/detail/get/detail?id=B0FFF9Q1I7
        self.GetPloy="https://www.amap.com/detail/get/detail?id=";
        #中国省份
        self.Provinces=["北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省",
                        "吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省",
                        "江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区",
                        "海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省",
                        "甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","台湾省","香港特别行政区","澳门特别行政区","未知"];
        #定义数据string
        self.Dic="";

    # 判断是否为数字
    def isNum(self,value):
        try:
            float(value)
        except BaseException:
            return False
        else:
            return True

    #处理数据
    def Read(self):
        count=0;
        pathStr=self.FilePathStr+self.Province+"/"+self.TypeCode+".txt";
        #打开文件
        f=open(pathStr,"r");
        #读取第一行
        line=f.readline();
        #判断是否存在数据
        count=0;
        while line:
            try:
                self.GetBuildId(line);
            except BaseException:
                print("GetBuildId报错")
            else:
                i=1;
            #判断数据属于哪个省份
            line=f.readline();
            count=count+1;
            if count%100==1:
                self.SaveStr();
                print("保存");
        #关闭文件
        f.close();
    
    #保存数据
    def SaveStr(self):
        #保存数据
        pathStr=self.SaveDir+self.Province+".csv";
        file=open(pathStr,'w');
        file.writelines(self.Dic);
        file.close();
        self.Dic="";
        print("保存完成");
    
    #http请求
    def GetData(self,url):
        try:
            request = requests.get(url=url, timeout=(5, 27));
            html = request.text;
            request.close();
            return html;
        except:
            return "";

    def GetBuildId(self,line):
        line = line.replace("\n", "")
        strs = line.split(',');
        x = 0;
        y = 0;
        if self.isNum(strs[6]):
            x = strs[6];
            y = strs[7];
        else:
            x = strs[7];
            y = strs[8];
        if self.isNum(y) != True:
            return ;

        url = self.BuildUrl + x + "," + y + "&words=" + strs[0];
        # print(url);
        strdata = self.GetData(url);
        jsonData = {}
        jsonData = json.loads(strdata);
        if jsonData["status"] != "1":
            return ;

        buildlist = jsonData["data"]["tip_list"];
        for build in buildlist:
            category = build["tip"]["category"]
            name = build["tip"]["name"]
            id = build["tip"]["id"]
            if name == strs[0] and category.find('12') == 0:
                try:
                    self.GetBuild(id, line)
                except BaseException:
                    print("GetBuild报错");
                else:
                    break;
                break;

    #获取建筑信息
    def GetBuild(self,buildId,line):
        #buildId="B0FFF9Q1I7";
        url=self.GetPloy+buildId;
        print(url);
        strdata = self.GetData(url);
        jsonData = json.loads(strdata);
        if ("mining_shape" in strdata) and ("shape" in strdata):
            shape=jsonData["data"]["spec"]["mining_shape"]["shape"]
            self.Dic+=line+","+jsonData["data"]["spec"]["mining_shape"]["area"]+",|["+shape+"]\n"
        #print(self.Dic);

if __name__=="__main__":
    #创建对象
    data=DataDispose();
    #执行
    data.Read();
    #保存
    data.SaveStr();

    #os.remove(pathStr);
    #print("删除文件");
    print("完成");