import numpy as np
import collections
 
#定义字典存放颜色分量上下限
#例如：{颜色: [min分量, max分量]}
#{'red': [array([160,  43,  46]), array([179, 255, 255])]}
 
def getColorList():
    dict = collections.defaultdict(list)
 
    # 黑色
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 254, 80])
    color_list = []
    color_list.append(lower_black)
    color_list.append(upper_black)
    dict['Black'] = color_list
 
    #灰色
    # lower_gray = np.array([0, 0, 46])
    # upper_gray = np.array([180, 43, 220])
    # color_list = []
    # color_list.append(lower_gray)
    # color_list.append(upper_gray)
    # dict['gray']=color_list
 
    # 白色
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['White'] = color_list
 
    #红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['Red']=color_list
 
    
    # 红色2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['Red2'] = color_list
    
 
    #橙色
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['Lime'] = color_list
 
    #黄色
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['Yellow'] = color_list
 
    #绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['Green'] = color_list
 
    #青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['Cyan'] = color_list
 
    #蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['Blue'] = color_list
 
    # 紫色
    lower_purple = np.array([120, 43, 46])
    upper_purple = np.array([170, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['Magenta'] = color_list
 
    return dict
 
 
if __name__ == '__main__':
    color_dict = getColorList()
    print(color_dict)
 
    num = len(color_dict)
    print('num=',num)
 
    for d in color_dict:
        print('key=',d)
        print('value=',color_dict[d][1])
