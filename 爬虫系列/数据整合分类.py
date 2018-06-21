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
        self.TypeCode="190000";#020000 5400000条
        #读取文件路径
        self.FilePathStr="F:/数据/第六批/";
        #保存文件路径
        self.SaveDir="F:/数据/整理/";
        #中国省份
        self.Provinces=["北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省",
                        "吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省",
                        "江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区",
                        "海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省",
                        "甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","台湾省","香港特别行政区","澳门特别行政区","未知"];
        #定义数据string
        self.Dic={};
        for item in self.Provinces:
            self.Dic[item]="";

    #处理数据
    def Dispose(self):
        count=0;
        pathStr=self.FilePathStr+self.TypeCode+".txt";
        #打开文件
        f=open(pathStr,"r");
        #读取第一行
        line=f.readline();
        line=f.readline();
        #判断是否存在数据
        while line:
            strs=line.split(',');
            strr=strs[9]+strs[10]+strs[11];
            #判断数据属于哪个省份
            province="未知";
            for item in self.Provinces:
                if item in strr:
                    province=item;
                    break;
            #保存到相应文件中
            count+=1;
            if count%10000==1:
                print("第"+str(count)+"条数据");
            if count%30000==1:
                self.SaveStr();
                
            self.Dic[province]+=line;
            line=f.readline();
        #关闭文件
        f.close();
    #保存数据
    def SaveStr(self):
        #遍历数据
        for key in self.Dic:
            #保存数据
            pathStr=self.SaveDir+key+"/"+self.TypeCode+".csv";
            file=open(pathStr,'a');
            file.writelines(self.Dic[key]);
            file.close();
            self.Dic[key]="";
            #print(key+"保存完成");                              
        print("保存完成");
        
        
if __name__=="__main__":
    #创建对象
    data=DataDispose();
    #执行
    data.Dispose();
    #保存
    data.SaveStr();
    pathStr=data.FilePathStr+data.TypeCode+".txt";
    os.remove(pathStr);
    print("删除文件");
    print("完成");