import cv2

fourcc = cv2.VideoWriter_fourcc(*'XVID')

videoWriter = cv2.VideoWriter('aa.avi', fourcc, 10, (700,525))
for i in range(100, 1604, 4):                                    #有多少张图片，从编号1到编号2629
    image_number = i
    img12 = cv2.imread('image/' + str(image_number) + '.png')
    videoWriter.write(img12)
videoWriter.release()
