"""
通过高德地图爬取POI数据-分割中国地块
由于高德矩形获取POI智能返回10000条数据，
所以将中国地图版块分割成小与1000的矩形框
"""
import requests,sys
import os;
import time
import json

#矩形框
class Rect:
    def __init__(self,xmin,ymin,xmax,ymax):
        self.xmin=xmin;
        self.ymin = ymin;
        self.xmax = xmax;
        self.ymax = ymax;

class Cut:
    def __init__(self):
        self.maxCount = 250;
        self.PageSize = 11;
        self.types="050000";
        self.CountRequest=0;
        self.filePath="MapPOI/rect/050000.txt";
        #self.Url="http://restapi.amap.com/v3/place/polygon?polygon=108.640287,26.043184;110.579374,27.275355&key=dc44a8ec8db3f9ac82344f9aa536e678&extensions=all&offset=5&page=1";
        self.Url = "http://restapi.amap.com/v3/place/polygon?polygon=";
    #切分地块
    def CutChina(self,rect):
        url=self.Url;
        url=self.Url+str(rect.xmin)+","+str(rect.ymin)+","+str(rect.xmax)+","+str(rect.ymax)+"&key=caaa086bdf5666322fba3baf5a6a2c03&extensions=all&offset=25&page=1&types="+self.types;
        #print(url);
        count=0;
        try:
            data = self.DownHtml(url=url);
            jsonData = json.loads(data);
            print(url);
            count=int(jsonData["count"]);
        except IOError:
            count = 0;
            print('请求错误')
        else:
            count = int(jsonData["count"]);
        self.CountRequest=self.CountRequest+1;
        print("第"+str(self.CountRequest)+"次请求--数量："+str(count));
        if count<self.maxCount:
            if count==0:
                return ;
            file=open(self.filePath,"a")
            file.writelines(str(rect.xmin)+","+str(rect.ymin)+","+str(rect.xmax)+","+str(rect.ymax)+"\n");
            file.close();
            print("写入数据");
        else:
            middleX=(rect.xmin+rect.xmax)/2;
            middleY = (rect.ymin + rect.ymax) / 2;
            rect1=Rect(xmin=rect.xmin,ymin=rect.ymin,xmax=middleX,ymax=middleY);
            rect2 = Rect(xmin=middleX, ymin=rect.ymin, xmax=rect.xmax, ymax=middleY);
            rect3 = Rect(xmin=rect.xmin, ymin=middleY, xmax=middleX, ymax=rect.ymax);
            rect4 = Rect(xmin=middleX, ymin=middleY, xmax=rect.xmax, ymax=rect.ymax);
            #使用递归调用
            time.sleep(0.1)  # 休眠0.1秒
            self.CutChina(rect=rect1);
            time.sleep(0.1)  # 休眠0.1秒
            self.CutChina(rect=rect2);
            time.sleep(0.1)  # 休眠0.1秒
            self.CutChina(rect=rect3);
            time.sleep(0.1)  # 休眠0.1秒
            self.CutChina(rect=rect4);
    #下载数据
    def DownHtml(self,url):
        request = requests.get(url=url, timeout=(5, 27));
        html = request.text;
        request.close();
        return html;

if __name__=="__main__":
    cut = Cut();
    #开始先创建矩形存储文件
    file=open(cut.filePath,"w+");
    file.writelines("xmin,ymin,xmax,ymax\n");
    file.close();
    #开始分割中国区域
    rect=Rect(xmin=71.234018,ymin=17.725738,xmax=136.139681,ymax=55.28893);
    cut.CutChina(rect);
    print("程序完成结束")
