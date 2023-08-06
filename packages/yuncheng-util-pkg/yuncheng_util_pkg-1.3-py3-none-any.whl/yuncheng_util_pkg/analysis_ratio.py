# 完成的功能是：
from yuncheng_util_pkg.util_file import label_yc_line_v2
# 1，将算法结果与图片进行结合，此时会标记出算法识别出来的ct区域
def show_ct_by_yc_result_and_pic(imdata_bgr,yc_jsonResult,saveName,position=0.2):
    label_yc_line_v2(imdata_bgr,yc_jsonResult,position,saveName)

