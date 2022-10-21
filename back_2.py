import cv2
import argparse
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


rospy.init_node('aaaaaaaaaaa', anonymous=True)
bridge = CvBridge()


def callback(data):
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        print("cv_image")
    except CvBridgeError as e:
        print(e)
        args = parser.parse_args()
    model = cv2.createBackgroundSubtractorMOG2()


    img_background = cv2.imread("image.png", 1)
    print(model)
    #mask = model.apply(img_background)
    mask = model.apply(frame)

    # 輪郭抽出する。
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # 小さい輪郭は除く
    contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))

    # 輪郭を囲む外接矩形を取得する。
    bboxes = list(map(lambda x: cv2.boundingRect(x), contours))

    # 矩形を描画する。
    for x, y, w, h in bboxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("mask", mask)
    cv2.waitKey(1)

# cap.release()
# cv2.destroyAllWindows()

def start_node():
    print("aaaaaa")

    image_sub = rospy.Subscriber("/hsrb/head_rgbd_sensor/rgb/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass
