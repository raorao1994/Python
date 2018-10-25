import os,sys;
import xlrd
import xlwt

srcPath="D:\\_1820temple_output_1015.xls";
targetPath="D:\\全国合并.xls";
savePath="D:\\temple.xls";

#获取sheet
def getSheet(filePath):
    book = xlrd.open_workbook(filePath)  # 打开一个excel
    sheet = book.sheet_by_index(0)  # 根据顺序获取sheet
    # sheet2 = book.sheet_by_name('case1_sheet')  # 根据sheet页名字获取sheet
    return sheet;

#数据对比
def comparativeData():
    srcSheet=getSheet(srcPath)
    targetSheet = getSheet(targetPath)

    #book = xlrd.open_workbook(savePath)  # 打开一个excel
    #saveSheet = book.sheet_by_index(0)  # 根据顺序获取sheet

    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    saveSheet=workbook.add_sheet('data')   # 创建sheet

    srcRows = srcSheet.nrows  # 获取excel里面有多少行
    targetRows=targetSheet.nrows #获取excel里面有多少行
    targetKeyList=[]

    #获取目标sheet的所有key
    for row in range(targetRows):
        city=targetSheet.cell(row,1).value #指定行和列获取数据
        title = targetSheet.cell(row, 2).value  # 指定行和列获取数据
        targetKeyList.append(city+","+title)


    #遍历源数据
    rowIndex=1
    for row in range(srcRows):
        city = srcSheet.cell(row, 8).value  # 指定行和列获取数据
        title = srcSheet.cell(row, 4).value  # 指定行和列获取数据
        key=city+","+title
        if key not in targetKeyList:
            # saveSheet.cell(rowIndex,0).value=rowIndex
            # saveSheet.cell(rowIndex, 1).value = srcSheet.cell(row, 8).value
            # saveSheet.cell(rowIndex, 2).value = srcSheet.cell(row, 4).value
            # val = srcSheet.cell(row, 11).value + "-" + srcSheet.cell(row, 20).value
            # saveSheet.cell(rowIndex, 3).value = val
            # saveSheet.cell(rowIndex, 4).value = srcSheet.cell(row, 16).value
            # saveSheet.cell(rowIndex, 5).value = srcSheet.cell(row, 15).value
            # saveSheet.cell(rowIndex, 6).value = srcSheet.cell(row, 21).value
            # saveSheet.cell(rowIndex, 7).value = srcSheet.cell(row, 2).value
            # saveSheet.cell(rowIndex, 8).value = srcSheet.cell(row, 27).value

            saveSheet.write(rowIndex,0,rowIndex)
            saveSheet.write(rowIndex, 1, srcSheet.cell(row, 8).value)
            saveSheet.write(rowIndex, 2, srcSheet.cell(row, 4).value)
            val = srcSheet.cell(row, 11).value + "-" + srcSheet.cell(row, 20).value
            saveSheet.write(rowIndex, 3, val)
            saveSheet.write(rowIndex, 4, srcSheet.cell(row, 16).value)
            saveSheet.write(rowIndex, 5, srcSheet.cell(row, 15).value)
            saveSheet.write(rowIndex, 6, srcSheet.cell(row, 21).value)
            saveSheet.write(rowIndex, 7, srcSheet.cell(row, 2).value)
            saveSheet.write(rowIndex, 8, srcSheet.cell(row, 26).value)
            rowIndex=rowIndex+1

    workbook.save(savePath)

if __name__=="__main__":
    print("开始");
    comparativeData()
    print("完成");
