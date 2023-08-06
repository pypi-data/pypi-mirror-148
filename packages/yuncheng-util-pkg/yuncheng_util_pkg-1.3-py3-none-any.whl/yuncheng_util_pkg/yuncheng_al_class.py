'''
孕橙算法所需要的输入输出想
'''
import json
from yuncheng_util_pkg.util_net import *
from yuncheng_util_pkg.util_file import *
from yuncheng_util_pkg.util import *
import os
import requests
import cv2
# class Serialize():
#     def jsonTran(self):
#         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
# class AlInput(Serialize):
#     def __init__(self,imdata,id):
#         self.imdata = imdata
#         self.id = id
#
# class AlOutput(Serialize):
#     def __init__(self, entries: dict = {}):
#         for k, v in entries.items():
#             if isinstance(v, dict):
#                 self.__dict__[k] = AlOutput(v)
#             else:
#                 self.__dict__[k] = v

def make_al_input(imdata,id):
    requestbody = {"file":imdata,"id":os.path.basename(id),"filepath":id}
    return requestbody

def make_pano_al_input(imdata,id,points,ossUrl):
    requestbody = {"file":imdata,"id":os.path.basename(id),"filepath":id,
                   'points':points,'ossUrl':ossUrl,'bucketName':'yunchenguslh'}
    return requestbody
def use_cache_for_request(url,id,session,useCache=False,savePath=None):
    if useCache is False or savePath is None:
        return post_for_request(url,id,session)
    make_dirs(savePath)
    filename = os.path.join(savePath,os.path.basename(id['id']).split('.')[0]+'.json')
    result = read_json(filename)
    if result is not None:
        return result
    result = post_for_request(url, id, session)
    if result == 'error':
        return None
    write_json(filename,result)
    return result

def ask_for_yuncheng_al(url,pics,useCache=False,savePath=None):
    '''

    :param url:
    :param pics:
    :return:
    '''
    session = requests.session()
    bodys = []
    for i in pics:
        try:
            imdata = read_pic_to_base64(i)
            id = i
            body = make_al_input(imdata,id)
            bodys.append(body)
        except Exception as e:
            print(e)

    results = []
    for i in bodys:
        try:
            result = use_cache_for_request(url,i,session,useCache,savePath)
            results.append({
                'id':i['filepath'],
                'result':result
            })
        except Exception as e:
            print(e)
    return results

def show_yuncheng_result(results):
    for i in results:
        path = i['id']
        result = i['result']
        imdata =cv2.imread(path)
        label_yc_line(imdata[:,:,::-1],result,title=os.path.basename(path))

def ask_for_yuncheng_pano_point_al(url,datas,useCache=False,savePath=None):
    '''
    提供了一个测试接口，该接口会去调用一个特殊接口，该接口接收的参数是一个全景图+几个坐标点，然后接口会把
    小图拿出来，然后进行计算，
    :param url:
    :param datas:[{'pic':path,'point':'[[1,1],[2,2],[1,2],[2,1]]',
    'ossUrl':'****.jpg'}]
    :return:
    '''
    session = requests.session()
    bodys = []
    for i in datas:
        try:
            imdata = read_pic_to_base64(i['pic'])
            point = i['points']
            ossUrl = i['ossUrl']
            id = i['pic']
            body = make_pano_al_input(imdata,id,point,ossUrl)
            bodys.append(body)
        except Exception as e:
            print(e)

    results = []
    for i in bodys:
        try:
            result = use_cache_for_request(url,i,session,useCache,savePath)
            results.append({
                'id':i['filepath'],
                'result':result
            })
        except Exception as e:
            print(e)
    return results