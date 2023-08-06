import cv2
import numpy as np
import matplotlib.pyplot as plt
def analysis_pic(path):
    imdata = cv2.imread(path)
    imdata = cv2.resize(imdata,(1080,90))
    imdata = imdata[40:50,400:600,:]

    imdata = cv2.blur(imdata,(5,1))


    imdata2 = cv2.cvtColor(imdata,cv2.COLOR_BGR2LAB)[:,:,0]
    info = np.sum(imdata2,axis=0)
    plt.subplot(211)
    plt.imshow(imdata[:,:,::-1])
    plt.subplot(212)
    # plt.xscale([0,200])
    plt.plot([i for i in range(len(info))],info)
    plt.title(path)
    plt.show()


def analysis_pic_line(path):
    imdata = cv2.imread(path)
    imdata2 = cv2.cvtColor(imdata,cv2.COLOR_BGR2LAB)[:,:,0]
    h,w = imdata2.shape
    plt.figure(figsize=(20,40))
    plt.subplot(511)
    plt.imshow(imdata[:,:,::-1])
    plt.subplot(512)
    plt.plot([i for i in range(w)],np.sum(imdata2[h//5:h//5+1,:],axis=0),color='r')
    plt.subplot(513)
    plt.plot([i for i in range(w)], np.sum(imdata2[h // 2:h // 2 + 1, :],axis=0),color='blue')
    plt.subplot(514)
    plt.plot([i for i in range(w)], np.sum(imdata2[h*4 // 5:h*4 // 5 + 1, :],axis=0),color='black')
    plt.subplot(515)
    plt.plot([i for i in range(w)],np.sum(imdata2[h//5:h//5+1,:],axis=0),color='r')
    plt.plot([i for i in range(w)], np.sum(imdata2[h // 2:h // 2 + 1, :],axis=0),color='blue')
    plt.plot([i for i in range(w)], np.sum(imdata2[h*4 // 5:h*4 // 5 + 1, :],axis=0),color='black')

    plt.title(path)
    plt.show()
