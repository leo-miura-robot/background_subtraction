from __future__ import print_function
import cv2 as cv
import argparse
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='test.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='KNN')

bridge = CvBridge()

rospy.init_node('listener', anonymous=True)

global cv_image

def callback(data):
    while True:
        try:
            
            frame = bridge.imgmsg_to_cv2(data, "bgr8")
            print("cv_image")
        except CvBridgeError as e:
            print(e)
            args = parser.parse_args()

        backSub = cv.createBackgroundSubtractorMOG2()


        #capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))




        fgMask = backSub.apply(frame)
        
        
        cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        #cv.putText(frame, str(cv_image.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
        
        
        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)
        
        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

def start_node():
    print("aaaaaa")
    image_sub = rospy.Subscriber("/hsrb/head_rgbd_sensor/rgb/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass


