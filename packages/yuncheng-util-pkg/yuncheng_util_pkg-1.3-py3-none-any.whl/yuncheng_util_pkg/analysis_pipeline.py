'''
对孕橙算法，第一阶段，第二阶段的pipeline进行图形化展示，单纯的看json，太费劲了！
'''
from yuncheng_util_pkg.util_net import get_for_request
from yuncheng_util_pkg.util_net import post_for_request
from yuncheng_util_pkg.util_file import down_pic
from yuncheng_util_pkg.yuncheng_al_class import ask_for_yuncheng_al
import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger("t")

def get_pipeline_error_info(id,savePath,url="http://192.168.1.222:12010/get-wrong-info/",checkUrl = 'http://192.168.1.222:8001/lh/lhRawdataAnalysis'):
    '''
     获取第二阶段算法pipeline的结果，并将识别错误的结果进行重复调用+结果展示
    :param id: 数据库中记录的本地执行的主键
    :param savePath: 结果保存的位置
    :param url: 调用的pipeline所在的地址
    :param checkUrl: 算法提供的接口的地址
    :return: 算法执行的结果

    '''
    ur = url+str(id)
    res = get_for_request(ur)
    _down_pipeline_info(res,savePath)
    return _ask_for_yuncheng(res,checkUrl)

def _down_pipeline_info(res:object,savepath:str):
    '''
    下载第二阶段pipeline wrong的返回结果到指定的路径，不单独使用
    :param res:
    :param savepath:
    :return:
    '''
    for i in res['result']:
        url = i['url']
        picpath = down_pic(url,savepath)
        i['path'] = picpath

def _ask_for_yuncheng(res:object,al_url):
    '''
    同样配合着上面获取第二阶段识别错误结果的接口使用
    :param res:
    :param al_url:
    :return:
    '''
    pics = [i['path'] for i in res['result']]
    result = ask_for_yuncheng_al(al_url,pics)
    for i in result:
        for k in res['result']:
            if i['id'] == k['path']:
                i['pipeinfo'] = k
                continue
    return result

def make_model(platform,sdkversion,modelVersion):
    return {"platform":platform,"sdkVersion":sdkversion,"modelVersion":modelVersion}
def drawbox(imdata,title,points,anno_start,anno_end,color=(0,0,255)):
    '''
    在图片上将point的点进行标记，
    :param imdata:
    :param title:
    :param points: 4个点的坐标
    :param anno_start: 打标箭头开始点
    :param anno_end: 打标记箭头结束点
    :param color:
    :return:
    '''
    if points is not None and len(points) > 0:
        try:
            # rect = cv2.minAreaRect(np.array(points))
            # print(rect)
            # box = cv2.boxPoints(rect)
            # print(box)
            boxArray = np.int0(points)
            print(boxArray)
            cv2.drawContours(imdata, [boxArray], 0, color, 5)
            plt.annotate(title, xy=anno_end, xytext=anno_start,
                         xycoords='data',
                         arrowprops=dict(facecolor='black', shrink=0.05)
                         )
        except Exception as e:
            print(e)
    else:
        plt.annotate(title, xy=anno_end, xytext=anno_start,
                     xycoords='data',
                     arrowprops=dict(facecolor='black', shrink=0.05)
                     )


def label_pic(result,pic):
    imdata = cv2.imread(pic)
    v1 = result['v1']
    v2 = result['v2']
    title1 = "v1-error:{}".format(v1['errorCode'])
    point1 = v1.get("points",[])
    title2 = "v2-error:{}".format(v2['errorCode'])
    point2 = v2.get("points", [])
    anno_start1 = (100,100)
    anno_start2 = (200,150)
    anno_end1 = (50,50)
    anno_end2 = (100,150)
    if point1 != []:
        anno_end1 = (point1[0][0],point1[0][1])
    if point2 != []:
        anno_end2 = (point2[0][0],point2[0][1])
    drawbox(imdata, title1, point1,anno_start1,anno_end1,color=(0,0,255))
    drawbox(imdata, title2, point2,anno_start2,anno_end2,color=(0,255,0))
    plt.title(pic)
    plt.imshow(imdata[:, :, ::-1])
    plt.show()
def get_cut_pipeline_info(model1,model2,savePath="pics",url="http://192.168.1.222:12010/get-paper-cut-compare-detail"):
    '''
    将第一阶段的识别结果进行下载，并进行绘图展示
    :param model1:
    :param model2:
    :param savePath:
    :param url:
    :return:
    '''
    result = post_for_request(url,{"model1":model1,"model2":model2})
    '''
    {
    "code": 200,
    "data": [{"url": "下载地址",
            "v1": {"errorCode": 0,"batch": 361,"type": 1,"points": [[72,154],[71,106],[182,103],[183,151]]},
            "v2": {"errorCode": 0,"batch": 361,"type": 1,"points": [[121,259],[119,178],[305,172],[308,253]]}
        }]
    }
    '''
    if result is None:
        return "error no info"
    for i in result['data'][20:40]:
        pic = down_pic(i['url'],savePath)
        label_pic(i,pic)


