# -*- coding: utf-8 -*-

import urllib2 as urllib
import numpy as np
import cv2

"""
需要和数据库交互存储头像信息么?
模块尽量职责单一, 因此不在 Python 中存储头像图片数据到数据库中.
"""
class OpencvThumbnail():

    def load_image_url(self, url):
        resp = urllib.urlopen(url)
        buf = resp.read()
        return buf

    def load_image_buffer(self, buffer):
        x = np.fromstring(buffer, dtype=np.uint8)
        nparray = np.fromstring(buffer, dtype=np.uint8)
        image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
        return image

    def get_dimension(self, image):
        height, width = image.shape[:2]
        return (width, height)

    def crop_landscape(self, image, dim):
        r = (dim[0] / image.shape[0]) / (dim[0] / dim[1])
        nw = int(image.shape[1] * r)
        resized = cv2.resize(image, (nw, int(dim[1])), interpolation=cv2.INTER_AREA)
        half_width = int(dim[0]) / 2
        half_shape_width = int(resized.shape[1]) / 2
        start_x = half_shape_width - half_width
        end_x = half_width + half_shape_width
        cropped = resized[0:dim[1], start_x:end_x]
        return cropped

    def crop_portrait(self, image, dim):
        r = dim[1] / image.shape[1] / (dim[1] / dim[0])
        nh = int(image.shape[0] * r)
        resized = cv2.resize(image, (int(dim[0]), nh), interpolation=cv2.INTER_AREA)
        half_height = int(dim[1]) / 2
        half_shape_height = int(resized.shape[0]) / 2
        start_y = half_shape_height - half_height
        end_y = half_height + half_shape_height
        cropped = resized[start_y:end_y, 0:dim[0]]
        return cropped

    def corp(self, image, dim):
        # 1 => width index, 0 => height index
        try:
            if image.shape[0] > image.shape[1]:
                cropped = self.crop_portrait(image, dim)
            else:
                cropped = self.crop_landscape(image, dim)
            return
        except Exception, ex:
            pass

    def fill(self, image, dim):
        pass

    def generate_avatars(self, image_buf):
        (height, width) = self.get_dimension()
        corp_sizes = []
        if height >= 1280:
            avatar_image = self.corp(image_buf, (1280, 1280))
            corp_sizes.append(avatar_image)
        if height >= 640:
            avatar_image = self.corp(image_buf, (640, 640))
            corp_sizes.append(avatar_image)
        if height >= 320:
            avatar_image = self.corp(image_buf, (320, 320))
            corp_sizes.append(avatar_image)
        if height >= 160:
            avatar_image = self.corp(image_buf, (160, 160))
            corp_sizes.append(avatar_image)
        if height < 160:
            # If the image dimension less than minimum required size,
            # fill surrounding with white space to minimum size.
            avatar_image = self.fill(image_buf, (160, 160))
            corp_sizes.append(avatar_image)
        return corp_sizes

