import os,sys;
import xlrd
import xlwt
from xlutils.copy import copy        #导入copy模块
from gensim import corpora, models, similarities
import jieba

srcPath="D:\\_1820temple_output_1015.xls";
targetPath="D:\\全国合并7.xls";
savePath="D:\\temple.xls";

#获取sheet
def getSheet(filePath):
    book = xlrd.open_workbook(filePath)  # 打开一个excel
    sheet = book.sheet_by_index(0)  # 根据顺序获取sheet
    # sheet2 = book.sheet_by_name('case1_sheet')  # 根据sheet页名字获取sheet
    return sheet;

def saveData(saveSheet,srcSheet,row,rowIndex):
    saveSheet.write(rowIndex, 0, rowIndex)
    saveSheet.write(rowIndex, 1, srcSheet.cell(row, 8).value)
    saveSheet.write(rowIndex, 2, srcSheet.cell(row, 4).value)
    val = srcSheet.cell(row, 11).value + "-" + srcSheet.cell(row, 20).value
    saveSheet.write(rowIndex, 3, val)
    saveSheet.write(rowIndex, 4, srcSheet.cell(row, 16).value)
    saveSheet.write(rowIndex, 5, srcSheet.cell(row, 15).value)
    saveSheet.write(rowIndex, 6, srcSheet.cell(row, 21).value)
    saveSheet.write(rowIndex, 7, srcSheet.cell(row, 2).value)
    saveSheet.write(rowIndex, 8, srcSheet.cell(row, 26).value)

#数据对比
def comparativeData():
    srcSheet=getSheet(srcPath)
    targetSheet = getSheet(targetPath)

    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    saveSheet=workbook.add_sheet('templeList')   # 创建sheet
    saveSheet1 = workbook.add_sheet('targetKeyList')  # 创建sheet

    srcRows = srcSheet.nrows  # 获取excel里面有多少行
    targetRows=targetSheet.nrows #获取excel里面有多少行
    #地区列表
    targetKeyList=[]
    #寺庙名列表
    templeList=[]

    #获取目标sheet的所有key
    for row in range(targetRows):

        address=targetSheet.cell(row,3).value #指定行和列获取数据
        city = targetSheet.cell(row, 1).value  # 指定行和列获取数据
        title = targetSheet.cell(row, 2).value  # 指定行和列获取数据
        targetKeyList.append(address+","+city)
        templeList.append(title)


    #遍历源数据
    rowIndex=1
    for row in range(srcRows):
        address = srcSheet.cell(row, 11).value  # 指定行和列获取数据
        city = srcSheet.cell(row, 8).value  # 指定行和列获取数据
        title = srcSheet.cell(row, 4).value  # 指定行和列获取数据
        key=address+","+city
        if title not in templeList:
            #保存数据
            saveData(saveSheet,srcSheet,row,rowIndex)
            rowIndex=rowIndex+1
        else:
            #文本内容对比
            print("地理位置对比！")
            isok=comparative(key,targetKeyList)
            if isok==False:
                saveData(saveSheet1, srcSheet, row, rowIndex)
                rowIndex = rowIndex + 1

        if row%100==0:
            print("第："+str(row))


    workbook.save(savePath)

# 分词函数，返回分词列表
def cut(sentence):
    generator = jieba.cut(sentence)
    return [word for word in generator]

#文字对比
def comparative(text,keyList):
    # 文本集和搜索词
    text1 = '吃鸡这里所谓的吃鸡并不是真的吃鸡，也不是我们常用的谐音词刺激的意思'
    text2 = '而是出自策略射击游戏《绝地求生：大逃杀》里的台词'
    text3 = '我吃鸡翅，你吃鸡腿'
    keyword = '玩过吃鸡？今晚一起吃鸡'
    texts=[text1,text2,text3]
    texts = keyList
    keyword=text
    # 1、将【文本集】生成【分词列表】
    texts = [cut(text) for text in texts]
    # 2、基于文本集建立【词典】，并提取词典特征数
    dictionary = corpora.Dictionary(texts)
    feature_cnt = len(dictionary.token2id.keys())
    # 3、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 4、使用【TF-IDF模型】处理语料库
    tfidf = models.TfidfModel(corpus)
    # 5、同理，用【词典】把【搜索词】也转换为【稀疏向量】
    kw_vector = dictionary.doc2bow(cut(keyword))
    # 6、对【稀疏向量集】建立【索引】
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
    # 7、相似度计算
    sim = index[tfidf[kw_vector]]
    for i in range(len(sim)):
        if(sim[i]>0.5):
            print('keyword 与 text%d 相似度为：%.2f' % (i + 1, sim[i]))
            return True;
    return False;

#对比寺庙名字
def tempCom(temp,tempList):
    for item in tempList:
        try:
            nPos = item.index(temp)
            if nPos>0:
                return True
        except:
            i=1
        else:
            i=2
        return False

#数据预处理
def initData():
    str1="山"
    srcSheet=getSheet("D:\\全国合并6.xls")
    srcRows = srcSheet.nrows  # 获取excel里面有多少行
    workbook = xlwt.Workbook(encoding='utf-8')
    saveSheet = workbook.add_sheet('data')  # 创建sheet
    #遍历数据
    for row in range(srcRows):
        text=srcSheet.cell(row,2).value #指定行和列获取数据
        try:
            nPos = text.index(str1)
            leng1=len(text)
            if nPos+3>leng1:
                nPos=-1
            if nPos>0:
                text = text[nPos + 1:]
        except:
            i=1
        else:
            i=2
        saveSheet.write(row, 0, srcSheet.cell(row,0).value)
        saveSheet.write(row, 1, srcSheet.cell(row,1).value)
        saveSheet.write(row, 2, text)
        saveSheet.write(row, 3, srcSheet.cell(row,3).value)
        saveSheet.write(row, 4, srcSheet.cell(row,4).value)
        saveSheet.write(row, 5, srcSheet.cell(row,5).value)
        saveSheet.write(row, 6, srcSheet.cell(row, 6).value)
        saveSheet.write(row, 7, srcSheet.cell(row, 7).value)
        saveSheet.write(row, 8, srcSheet.cell(row, 8).value)
        if row%100==0:
            print("第"+str(row))
    workbook.save("D:\\全国合并7.xls")  # 保存文件

if __name__=="__main__":
    print("开始");
    #initData()
    comparativeData()
    print("完成");
