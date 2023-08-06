# 对比比色卡结果
# 整个过程是：算法会接收标注了CT以及比色卡位置的图片。
# 从中提取出CT的最深区域的均值，以及比色卡位置的上的均值，然后进行对比
# colorboard 的配置文件，由于colorboard会有区别，所以一配置的形式进行填充
import json
import cv2
from collections import Counter
import numpy as np
david_config = {"3":2.5,"4":5,"5":10,"6":15,"7":20,"8":25,"9":40,"10":65,"11":80}
david_index = [2.5,5,10,15,20,25,40,65,80]
ct_config = {"T":"2","C":"1"}
color_type = [1,2,3]
def imshow(imdata):
    h,w,c = imdata.shape
    if h > 400:
        w = 400*w//h
        h = 400
    imdata2 = cv2.resize(imdata,[w,h])
    cv2.imshow("ws",imdata2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def read_label(label_path):
    '''
    读取labelme标注的图片结果
    :param label_path: 标记的位置
    :return: {"C":[[],[]],"T":[[],[]],"label":[从小到大每个标记点的位置]}
    '''
    with open(label_path,'r') as f:
        dataStr = f.read()
    dataObj = json.loads(dataStr)
    shapes = dataObj['shapes']
    shapesDir = {}
    result = {}
    for i in shapes:
        shapesDir[i['label']] = i['points']
    result['T'] = shapesDir[ct_config['T']]
    result['C'] = shapesDir[ct_config['C']]
    result['label'] = []
    for i in david_config:
        result['label'].append(shapesDir[i])
    return result

def get_deepest_y_loc(imc):
    im = cv2.cvtColor(imc, cv2.COLOR_BGR2LAB)
    im = im[:, :, 0]
    im = np.sum(im, axis=0)
    deep_loc = np.where(im==np.min(im))[0][0]
    return deep_loc
def get_deepest_y_ave(imdata,loc,type=1):
    '''
    获取指定区域最深色像素位置的均值
    :param imdata: 通过opencv读到的信息，bgr格式
    :param loc:[[x,y],[lengthx,lengthy]]
    :param type: 指定返回的颜色空间，
    :return:
    '''
    check_color = imdata[int(loc[0][1]):int(loc[1][1]),int(loc[0][0]):int(loc[1][0]),:]
    deepst_loc = get_deepest_y_loc(check_color)
    if type == 1:
        # RGB
        check_color = cv2.cvtColor(check_color,cv2.COLOR_BGR2RGB)
        check_color = check_color[:,:,0]
        im = np.average(check_color,axis=0)
        return im[deepst_loc]
    elif type == 2:
        check_color = cv2.cvtColor(check_color,cv2.COLOR_BGR2GRAY)
        im = np.average(check_color,axis=0)
        return im[deepst_loc]
    elif type == 3:
        check_color = cv2.cvtColor(check_color,cv2.COLOR_BGR2LAB)
        check_color1 = check_color[:,:,0]
        im = np.average(check_color1,axis=0)
        check_color2 = check_color[:, :, 1]
        im2 = np.average(check_color2, axis=0)
        check_color3 = check_color[:, :, 2]
        im3 = np.average(check_color3, axis=0)

        # return np.sum(im)/len(im)
        return im[deepst_loc] + im2[deepst_loc] + im3[deepst_loc]
    return 0

def check(picpath,label_path,type,fig=None):
    imdata = cv2.imread(picpath)
    label_info = read_label(label_path)
    T = label_info['T']
    label = label_info["label"]
    T_ave = get_deepest_y_ave(imdata,T,type)
    label_ave = []
    for i in label:
        ave = get_deepest_y_ave(imdata,i,type)
        label_ave.append(ave)
    if fig is not None:
        fig.plot([i for i in range(len(label_ave))],label_ave)
        fig.plot([i for i in range(len(label_ave))],[T_ave for i in range(len(label_ave))])
        for x, y in enumerate(label_ave):
            plt.text(x, y, f'{round(y,3)}')
        fig.show()
    print(f"T:{T_ave},label:{label_ave}")
    T_ave = [T_ave] * len(label_ave)
    d = abs(np.subtract(T_ave, label_ave))
    index = np.where(d == np.min(d))[0][0]
    print(np.min(d))
    return david_index[index]

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    p = r"D:\BaiduNetdiskDownload\picture\picture\iphone\iphone_pos1_"
    pics = [ p + f"{i}.JPG" for i in range(21,41)]
    labels = [ p + f"{i}.json" for i in range(21,41)]
    z = zip(pics,labels)
    res = []
    for i in z:
        res.append(check(i[0],i[1],3,plt))
    print(Counter(res))
    # picpath = r"D:\BaiduNetdiskDownload\picture\picture\android\android_pos1_1.JPG"
    # label_path = r"D:\BaiduNetdiskDownload\picture\picture\android\android_pos1_1.json"



