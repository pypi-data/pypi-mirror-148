'''
该文档是一个总结性的，通过调用数据提供接口，可以下载该接口提供的图片数据，然后将这些数据调用要比较的算法
最后会得到一个汇总结果
'''
from yuncheng_util_pkg.util_net import get_for_request
from yuncheng_util_pkg.util_file import  down_pic
from yuncheng_util_pkg.compare_two_al_result import Get_result_and_compare
from yuncheng_util_pkg.compare_two_al_result import DecodeTheSummaryFile
import os
def get_pics(url,savePath):
    result = get_for_request(url)
    pics = []
    for i in result['data']:
        picUrl = i['url']
        pic = down_pic(picUrl,savePath)
        pics.append(pic)
    return pics

def compare(pics,url1,url2,savePath='compare_result',summaryFileName='summary_result.txt',url1ResultName='url1.txt',url2ResultName='url2.txt',useCache=True,getSameData=False):
    if os.path.exists(savePath) is False:
        os.makedirs(savePath)
    summaryFile = os.path.join(savePath,summaryFileName)
    url1ResultSavePath = os.path.join(savePath,url1ResultName)
    url2ResultSavePath = os.path.join(savePath,url2ResultName)
    com = Get_result_and_compare(url1,url2,pics,summaryFile,useCache,url1ResultSavePath,url2ResultSavePath)
    com.compare_two_pic_local()
    com.summary(getSameData)
    decodeSavePath = os.path.join(savePath,'decode')
    if os.path.exists(decodeSavePath) is False:
        os.makedirs(decodeSavePath)
    sameDataPath = None
    if getSameData:
        sameDataPath = os.path.join(savePath,'sameDataSave')
        if os.path.exists(sameDataPath) is False:
            os.makedirs(sameDataPath)

    dif = DecodeTheSummaryFile(summaryFile,decodeSavePath,sameDataPath)
    dif.show_brand_dif()
    dif.show_line_dir()
    dif.show_direction_dif()
    dif.show_value_dif()
    if getSameData:
        dif.get_line_same()
        dif.get_brand_same()
        dif.get_direction_same()
        dif.get_value_same()
