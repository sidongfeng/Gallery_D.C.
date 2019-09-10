import  cv2
import colorList as colorList
from PIL import Image
import numpy as np

def cv_imread(file_path):
    cv_img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)  
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化  
    ##cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)  
    return cv_img  

# return color area percentage
def get_color(path):
    frame = cv2.imread(path)
    
    #area = frame.shape[0]*frame.shape[1]
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    areadic = {}
    color_dict = colorList.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        #cv2.imwrite(d+'.jpg',mask)
        #binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        #binary = cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        # cv2.imwrite(d+'.png',binary)
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        #binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # 开运算
        binary = cv2.dilate(binary,None,iterations=0)
        img,cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imwrite(d+'.png',img)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        areadic[d] = sum
    
    # areadic['Red'] += areadic['Red2']
    # del areadic['Red2']

    area = 0
    for c in areadic.keys():
        area += areadic[c]
    if area == 0:
        return 0
    for c in areadic.keys():
        areadic[c] = round(areadic[c]/area,2)

    #sorted_area = sorted(areadic.items(), key=lambda d: d[1], reverse=True) 
    return areadic

if __name__ == '__main__':

    # img = '/Users/mac/Documents/Python/Rico/ImageButton-13028.png'
    # get_color(img)
    None