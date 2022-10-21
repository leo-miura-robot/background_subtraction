from __future__ import print_function
import cv2
import argparse
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='test.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='KNN')

bridge = CvBridge()

rospy.init_node('listener', anonymous=True)


def callback(data):
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        print("cv_image")
    except CvBridgeError as e:
        print(e)
        args = parser.parse_args()

    backSub = cv2.createBackgroundSubtractorMOG2(history=200, nmixtures=5, backgroundRatio=0.7, noiseSigma=0)
    fgMask = backSub.apply(frame)

    # # 輪郭抽出する。
    # contours = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # # 小さい輪郭は除く
    # contours = list(filter(lambda x: cv2.contourArea(x) > 2000, contours))

    # # 輪郭を囲む外接矩形を取得する。
    # bboxes = list(map(lambda x: cv2.boundingRect(x), contours))

    # # 矩形を描画する。
    # for x, y, w, h in bboxes:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fgMask)
    
    keyboard = cv2.waitKey(30)
    # if keyboard == 'q' or keyboard == 27:
    #     break

def start_node():
    print("aaaaaa")
    image_sub = rospy.Subscriber("/hsrb/head_rgbd_sensor/rgb/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass


