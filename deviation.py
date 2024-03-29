import numpy as np
import cv2

minMatchCount = 10
bestDeviation = 4
subDeviation = 10

# cv2内置的提取特征的方法
algorithms_all = {
    "SIFT": cv2.SIFT_create(),
#    "SURF": cv2.SURF_create(8000),
    "ORB": cv2.ORB_create()
}

'''
类别0: 完全不匹配
类别1: 场景匹配
类别2: 角度轻微偏移
类别3: 完全匹配
'''
def matchFrames(img1, img2):
    # BGR 图片转 Gray
    image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    size1 = image1.shape
    size2 = image2.shape

    image1 = cv2.resize(image1, (int(size1[1]*0.3), int(size1[0]*0.3)), cv2.INTER_LINEAR)
    image2 = cv2.resize(image2, (int(size2[1]*0.3), int(size2[0]*0.3)), cv2.INTER_LINEAR)

    sift = algorithms_all["SIFT"]

    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # 匹配各类
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) <= minMatchCount:
        return 0  # 完全不匹配
    else:
        distance_sum = 0  # 特征点2d物理坐标偏移总和
        for m in good:
            distance_sum += getDistance(kp1[m.queryIdx].pt, kp2[m.trainIdx].pt)
            distance = distance_sum / len(good)  # 单个特征点2D物理位置平均偏移量

            if distance < bestDeviation:
                return 3  # 完全匹配
            elif distance < subDeviation and distance >= bestDeviation:
                return 2  # 部分偏移
            else:
                return 1 # 场景匹配

def getDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# if __name__=="__main__":
#     pass




