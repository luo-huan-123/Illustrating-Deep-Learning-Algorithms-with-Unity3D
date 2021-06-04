#!/usr/bin/env python

# Standard modules
import socket
# External modules
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CompressedImage, CameraInfo
import numpy as np
# Local imports
import utils


class SendImage:

    def __init__(self):
        hostname = rospy.get_param('~hostname', 'localhost')
        port = rospy.get_param('~port', 6008)
        self.max_depth = rospy.get_param('~max_depth', 10.)

        self.jpeg_handler = utils.CV2JpegHandler(jpeg_quality=100)

        # A temporary buffer in which the received data will be copied
        # this prevents creating a new buffer all the time
        self.tmp_buf = bytearray(7)
        # this allows to get a reference to a slice of tmp_buf
        self.tmp_view = memoryview(self.tmp_buf)

        # Creates a temporary buffer which can hold the largest
        # image we can transmit
        self.img_buf = bytearray(9999999)
        self.img_view = memoryview(self.img_buf)

        rospy.loginfo("Connecting to {}:{}".format(hostname, port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))
        rospy.loginfo("connected !")

        # Publishers and subscribers
        self.segmentation_publisher = rospy.Publisher('/depth/image/compressed',
                                                                CompressedImage,
                                                                queue_size=1)
        self.image_subscriber = rospy.Subscriber('/image_in/compressed',
                                                 CompressedImage,
                                                 self.send_image,
                                                 queue_size=1,
                                                 buff_size=2**22)
    def send_image(self, in_img):
        """
        Sends the image to the server for processing it
        """
        compressed_in = np.fromstring(in_img.data, np.uint8)
        self.rgb_image = cv2.imdecode(compressed_in, cv2.IMREAD_COLOR)
        # print(self.rgb_image.shape)
        # width = self.rgb_image.shape[1]
        # cropped = self.rgb_image[:, (width//2 - 320):(width//2 + 320)]

        img_buffer = self.jpeg_handler.compress(self.rgb_image) 
        # Preparing the message with the number of bytes going to be sent
        # img_buffer=compressed_in
        msg = bytes("image{:07}".format(len(img_buffer)))
        utils.send_data(self.sock, msg)  # send the size
        utils.send_data(self.sock, img_buffer)  # send the data

        # Read the reply command
        utils.recv_data_into(self.sock, self.tmp_view[:5], 5)
        cmd = self.tmp_buf[:5].decode('ascii')

        if cmd != 'image':
            raise RuntimeError("Unexpected server reply")

        # Read the image buffer size
        utils.recv_data_into(self.sock, self.tmp_view, 7)
        img_size = int(self.tmp_buf.decode('ascii'))

        # Read the image buffer
        utils.recv_data_into(self.sock, self.img_view[:img_size], img_size)

        # Read the final handshake
        cmd = utils.recv_data(self.sock, 5).decode('ascii')
        if cmd != 'enod!':
            raise RuntimeError("Unexpected server reply. Expected 'enod!'"
                               ", got '{}'".format(cmd))
        # print(img_size)
        # Publish the depth image we receive
        # With [0, 255] values
        compressed_depth = CompressedImage()
        compressed_depth.header.stamp = rospy.Time.now()
        compressed_depth.format = "jpeg"
        compressed_depth.data = self.img_view[:img_size].tobytes()
        self.segmentation_publisher.publish(compressed_depth)


if __name__ == '__main__':
    rospy.init_node('send_video')
    SendImage()
    rospy.spin()