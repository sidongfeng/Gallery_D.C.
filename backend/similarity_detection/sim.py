import numpy
from skimage.measure import compare_ssim

def _calc_colour_hist(img):
    """
    使用L1-norm归一化获取图像每个颜色通道的25 bins的直方图，这样每个区域都可以得到一个75维的向量
    
    calculate colour histogram for each region

    the size of output histogram will be BINS * COLOUR_CHANNELS(3)

    number of bins is 25 as same as [uijlings_ijcv2013_draft.pdf]

    extract HSV
    
    args:
        img：ndarray类型， 形状为候选区域像素数 x 3(h,s,v)
        
    return：一维的ndarray类型，长度为75
            
    """

    BINS = 25
    hist = numpy.array([])

    for colour_channel in (0, 1, 2):

        # extracting one colour channel
        c = img[:, colour_channel]

        # calculate histogram for each colour and join to the result  
        #计算每一个颜色通道的25 bins的直方图 然后合并到一个一维数组中
        hist = numpy.concatenate(
            [hist] + [numpy.histogram(c, BINS, (0.0, 255.0))[0]])

    # L1 normalize  len(img):候选区域像素数
    hist = hist / len(img)

    return hist

def _calc_texture_hist(img):
    """
    使用L1-norm归一化获取图像每个颜色通道的每个方向的10 bins的直方图，这样就可以获取到一个240（10x8x3）维的向量
    
    calculate texture histogram for each region

    calculate the histogram of gradient for each colours
    the size of output histogram will be
        BINS * ORIENTATIONS * COLOUR_CHANNELS(3)
        
    args:
        img：候选区域纹理特征   形状为候选区域像素数 x 4(r,g,b,(region))
        
    return：一维的ndarray类型，长度为240
    """
    BINS = 10

    hist = numpy.array([])

    for colour_channel in (0, 1, 2):

        # mask by the colour channel
        fd = img[:, colour_channel]

        # calculate histogram for each orientation and concatenate them all
        # and join to the result
        hist = numpy.concatenate(
            [hist] + [numpy.histogram(fd, BINS, (0.0, 1.0))[0]])

    # L1 Normalize   len(img):候选区域像素数
    hist = hist / len(img)

    return hist

def _sim_colour(r1, r2):
    """
    计算颜色相似度

    calculate the sum of histogram intersection of colour
    
    args:
        r1：候选区域r1
        r2：候选区域r2
        
    return：[0,3]之间的数值
                
    """
    return sum([min(a, b) for a, b in zip(r1["hist_c"], r2["hist_c"])])


def _sim_texture(r1, r2):
    """
    计算纹理特征相似度
    
    calculate the sum of histogram intersection of texture
    
    args:
        r1：候选区域r1
        r2：候选区域r2
        
    return：[0,3]之间的数值
    
    """
    return sum([min(a, b) for a, b in zip(r1["hist_t"], r2["hist_t"])])


def _sim_size(r1, r2, imsize):
    """
    计算候选区域大小相似度
    
    calculate the size similarity over the image
    
    args:
        r1：候选区域r1
        r2：候选区域r2
        
    return：[0,1]之间的数值
    
    """
    return 1.0 - (r1["size"] + r2["size"]) / imsize


def _sim_fill(r1, r2, imsize):
    """
    计算候选区域的距离合适度相似度
    
    calculate the fill similarity over the image
    
    args:
        r1：候选区域r1
        r2：候选区域r2
        imsize：原图像像素数
        
    return：[0,1]之间的数值
    
    """
    bbsize = (
        (max(r1["max_x"], r2["max_x"]) - min(r1["min_x"], r2["min_x"]))
        * (max(r1["max_y"], r2["max_y"]) - min(r1["min_y"], r2["min_y"]))
    )
    return 1.0 - (bbsize - r1["size"] - r2["size"]) / imsize


def _calc_sim(r1, r2, imsize=None):
    '''
    计算两个候选区域的相似度，权重系数默认都是1
    
    args:
        r1：候选区域r1
        r2：候选区域r2
        imsize：原图片像素数
    '''
    return _sim_colour(r1, r2) + _sim_texture(r1, r2)
    # return (_sim_colour(r1, r2) + _sim_texture(r1, r2)
    #         + _sim_size(r1, r2, imsize) + _sim_fill(r1, r2, imsize))

def _sim_structure(r1, r2):
    return compare_ssim(r1["img"], r2["img"], full=True)[0]*3

if __name__ == "__main__":
    from skimage import io
    from scipy.ndimage import imread
    import matplotlib.pyplot as plt


