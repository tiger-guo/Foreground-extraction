import cv2
import numpy as np
import matplotlib.pyplot as plt
# Step1. 构造VideoCapture对象
def white_balance(frame):
    (B,G,R) = cv2.split(frame)
    aB = cv2.mean(B)[0]
    aG = cv2.mean(G)[0]
    aR = cv2.mean(R)[0]
    aA = (aB + aG + aR)/3
    kB = aA/aB+1
    kG = aA/aG+1
    kR = aA/aR+1
    B = cv2.addWeighted(B,kB,0,0,0)
    G = cv2.addWeighted(G,kG,0,0,0)
    R = cv2.addWeighted(R,kR,0,0,0)
    return cv2.merge((B,G,R))


def show(path_org,path = './result/result.avi',key = 0):
    name = path_org.split('/')[-1].split('.')[0]
    cap = cv2.VideoCapture(path)
    cap2 = cv2.VideoCapture(path_org)
    kernel = cv2.getStructuringElement(cv2.MORPH_OPEN,(3,3))
    sz = 0
    cnt = 1
    image_list = []
    while True  :
        ret,frame = cap.read()
        if frame is None:
            break
        _,frame_org = cap2.read()

        frame_org = cv2.resize(frame_org, (480, 320))
        frame_open = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        frame_re = cv2.resize(frame_open, (480, 320))
        frame_con = cv2.cvtColor(frame_re,cv2.COLOR_BGR2GRAY)
        n, m, _ = frame.shape
        sz = n * m
        image, contours, hcy = cv2.findContours(frame_con, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_sum = 0
        for i in range(0,len(contours)):
            if cv2.contourArea(contours[i]) > 600:
                c = [contours[i]]
                cv2.drawContours(frame_re,c,-1,(255,255,255),cv2.FILLED)
            area_sum += cv2.contourArea(contours[i])

        if 0.01 < area_sum / sz < 0.8:
            image_list.append((frame_re,cnt,area_sum))

        frame_rec = draw_rec(frame_org,contours)
        imgs = np.hstack([frame_rec,cv2.cvtColor(frame_re[:,:,0],cv2.COLOR_GRAY2BGR)])
        cv2.imshow("result",imgs)
        cnt += 1
        k = cv2.waitKey(10)
        if k & 0xff == ord('q'):
            break
        if k == 32:
            cv2.imwrite('./result/' + name + '_' + str(cnt) + ".jpg",imgs)
            print('已保存')
    cap.release()
    cv2.destroyAllWindows()
    image_list_size = len(image_list)
    for i in range(0, image_list_size):
        for j in range(i + 1, image_list_size):
            if image_list[i][2] < image_list[j][2]:
                image_list[i], image_list[j] = image_list[j], image_list[i]
    k = int(image_list_size**0.5)
    k = min(k,5)
    # plt.figure(figsize=(k,k))
    video_list = []
    plt.figure('关键帧')
    for i in range(0,min(k*k,30)):
        plt.subplot(k,k,i+1).imshow(image_list[i][0],cmap='gray',interpolation='nearest', aspect='auto')
        plt.title(image_list[i][1])
        temp_img = cv2.resize(image_list[i][0].copy(),(480,360))
        video_list.append((temp_img,image_list[i][1]))
        plt.axis('off')
    plt.show()
    if key == 1 :
        for i in range(0,len(video_list)):
            for j in range(0,len((video_list))):
                if video_list[i][1] < video_list[j][1]:
                    video_list[i],video_list[j] = video_list[j],video_list[i]
        videoWriter = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30.0, (480, 360), 1)
        for img in video_list:
            #img[0] = cv2.resize(img[0], (480, 360))
            videoWriter.write(img[0])
            print(img[1])
        videoWriter.release()
def draw_rec(frame,contours):
    res = frame
    for c in contours:
        if cv2.contourArea(c) > 500:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(res, (x, y), (x + w, y + h), (0, 0, 255), 1)
    return res
def capture(path,key = 0):
    name = path.split('/')[-1].split('.')[0]
    cap = cv2.VideoCapture(path)
    knn = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    ker = cv2.getStructuringElement(cv2.MORPH_OPEN,(3,3))
    frame_list = []
    th_area = 500
    frame_cnt = 1
    while True :
        ret, frame = cap.read() # 读取视频
        if frame is None:
            break
        frame =cv2.resize(frame,(480,360))      #方便显示
        res = cv2.GaussianBlur(frame,(3,3),3)   #高斯滤波预处理
        fgmask = knn.apply(res) # 背景分割
        th = cv2.threshold(fgmask.copy(),244,255,cv2.THRESH_BINARY)[1] #去除阴影
        th = cv2.morphologyEx(th,cv2.MORPH_OPEN,ker) # 开运算预处理
        image,contours,hcy = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # 获取轮廓
        area_sum = 0
        for i in range(0,len(contours)):
            #print(cv2.contourArea(contours[i]))
            if cv2.contourArea(contours[i]) > 600:
                c = [contours[i]]
                cv2.drawContours(th,c,-1,(255,255,255),cv2.FILLED)
            area_sum += cv2.contourArea(contours[i])
            if 0.01 < area_sum / (480 * 360) < 0.6:
                frame_list.append((th, frame_cnt, cv2.contourArea(contours[i])))


        frame_rec = draw_rec(res,contours)
        imgs = np.hstack([frame_rec,cv2.cvtColor(th,cv2.COLOR_GRAY2BGR)])
        cv2.imshow("result",imgs)

        frame_cnt += 1
        k = cv2.waitKey(10)
        if k & 0xff == ord('q'):
            break
        if k == 32:
            cv2.imwrite('./result/' + name + '_' + str(frame_cnt) + ".jpg", imgs)
            print('saved')
    cap.release()
    cv2.destroyAllWindows()

    if key == 1:
        image_list_size = len(frame_list)
        for i in range(0, image_list_size):
            for j in range(i + 1, image_list_size):
                if frame_list[i][2] < frame_list[j][2]:
                    frame_list[i], frame_list[j] = frame_list[j], frame_list[i]
        plt.figure('关键帧')
        video_list = []
        for i in range(0, min(image_list_size,20)):
            plt.subplot(4, 5, i + 1).imshow(frame_list[i][0], cmap='gray', interpolation='nearest', aspect='auto')
            plt.title(frame_list[i][1])
            video_list.append((frame_list[i][0],frame_list[i][1]))
            plt.axis('off')

        for i in range(0,len(video_list)):
            for j in range(0,len((video_list))):
                if video_list[i][1] < video_list[j][1]:
                    video_list[i],video_list[j] = video_list[j],video_list[i]
        videoWriter = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (480, 360), 0)
        for img in video_list:
            videoWriter.write(img[0])
            print(img[1])
        videoWriter.release()
        plt.show()


