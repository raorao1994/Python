# -*- coding: utf-8 -*-
"""
Created on Sat May 19 07:59:29 2018

@author: Administrator
"""

import os;
import json;

class DataDispose:
    
    def __init__(self):
        #类型code
        self.TypeCode="110000";
        self.Code="110205";
        #读取文件路径
        self.FilePathStr="G:/数据/整理/";
        #保存文件路径
        self.SaveDir="G:/数据/整理/寺庙/";
        #中国省份
        self.Provinces=["北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省",
                        "吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省",
                        "江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区",
                        "海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省",
                        "甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","台湾省","香港特别行政区","澳门特别行政区","未知"];
        #定义数据string
        self.Data="";

    #处理数据
    def Dispose(self,province):
        count=0;
        pathStr=self.FilePathStr+province+"/"+self.TypeCode+".csv";
        #打开文件
        f=open(pathStr,"r");
        #读取第一行
        line=f.readline();
        line=f.readline();
        #判断是否存在数据
        while line:
            strs=line.split(',');
            strr=strs[2]+strs[3]+strs[4];
            #判断数据属于哪个省份
            if self.Code in strr:
                self.Data+=line;
            #保存到相应文件中
            count+=1;
            if count%10000==1:
                print("第"+str(count)+"条数据");
            if count%30000==1:
                self.SaveStr(province);
            line=f.readline();
        self.SaveStr(province);
        #关闭文件
        f.close();
    #保存数据
    def SaveStr(self,province):
        #保存数据
        pathStr=self.SaveDir+province+".csv";
        file=open(pathStr,'a');
        file.writelines(self.Data);
        file.close();
        self.Data="";           
        print("保存完成");

    #操作所有数据
    def Run(self):
        for item in self.Provinces:
            self.Dispose(item);
if __name__=="__main__":
    #创建对象
    data=DataDispose();
    #执行
    data.Run();
    print("完成");