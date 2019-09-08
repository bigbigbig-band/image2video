# coding: utf-8

import os
import random
import time

import cv2

class ImageConvert2Video(object):
    def __init__(self, path, dst_resolution, dst_fps, dst_path, dst_name):
        self.image_list = [self.resize_scale(image, dst_resolution) for image in self._get_all_image(path)]
        self.video_resolution = dst_resolution
        
    def _get_all_image(self, path: str) -> list:
        if not os.path.exists(path):
            raise Exception("The path is not exitsts")
        return [cv2.imread(os.path.join(path, name)) for name in os.listdir(path)]
    
    def _get_max_shape(self, image) -> tuple:
        "获得组内最大的宽和高"
        max_h = 0
        max_w = 0
        for i in range(len(self.image_list)):
            if image[i].shape[0] > max_h:
                max_h = image[i].shape[0]
            if image[i].shape[1] > max_w:
                max_w = image[i].shape[1]
        return  max_w,max_h
    
    
    def _get_videowrite_obj(self) -> object:
         return cv2.VideoWriter("mytest.avi", cv2.VideoWriter_fourcc(*'XVID'), 18, self.video_resolution)
    
    
    def resize_scale(self, src, dst_resolution):
        "按比例缩小或者放大图片，指定一个大小值，自动按比例进行缩放或者放大"
        size = src.shape
        if dst_resolution[0] == dst_resolution[1]:
            if size[0] == size[1]:
                "图片宽高相等"
                scale = dst_resolution[0]/size[0]
                return cv2.resize(src, dsize=(0,0), fx=scale, fy=scale)
            
            if size[0] > size[1]:
                "高大于宽"
                scale = dst_resolution[0]/size[0]
                return cv2.resize(src, dsize=(0,0), fx=scale, fy=scale)
            else:
                "宽大于高"
                scale = dst_resolution[1]/size[1]
                return cv2.resize(src, dsize=(0,0), fx=scale, fy=scale)
        else:
            if size[0] == size[1]:
                "图片宽高相等"
                scale = min(dst_resolution) / size[0]
                return cv2.resize(src, dsize=(0, 0), fx=scale, fy=scale)
    
            if size[0] > size[1]:
                "高大于宽"
                scale = dst_resolution[0] / size[0]
                return cv2.resize(src, dsize=(0, 0), fx=scale, fy=scale)
            else:
                "宽大于高"
                scale = dst_resolution[1] / size[1]
                return cv2.resize(src, dsize=(0, 0), fx=scale, fy=scale)
            
    def _get_offset_list(self, video_height, offset, remainder, src_height) -> list:
        offset_list = []
        temp = 0
        while True:
            if temp + video_height > src_height:
                break
            offset_list.append([temp, temp+video_height])
            temp += offset
            
        temp = [offset_list.pop(0), offset_list.pop(-1)]
        random.shuffle(offset_list)
        for i in range(remainder):
            offset_list[i][0] += 1
            offset_list[i][1] += 1
        offset_list.extend(temp)
        offset_list.sort()
        offset_list = [tuple(offset) for offset in offset_list]
        return offset_list
        
    def up2down(self, src, image_num, video_resolution):
        if src.shape[1] < video_resolution[1]:
            raise Exception("The height is so little")
        else:
            sub = src.shape[1] - video_resolution[1]
            offset = 1 if sub // image_num == 0 else sub // image_num
            remainder = sub % image_num
            offset_list = self._get_offset_list(video_resolution[1], offset, remainder, src.shape[0])
            image_list = [src[offset[0]:offset[1], :] for offset in offset_list]
            return image_list
    
    def down2up(self, src, image_num, video_resolution):
        if src.shape[1] < video_resolution[1]:
            raise Exception("The height is so little")
        else:
            print(src.shape)
            sub = src.shape[1] - video_resolution[1]
            offset =  sub // image_num
            remainder = sub % image_num
            offset_list = self._get_offset_list(video_resolution[1], offset, remainder, src.shape[0])
            offset_list.sort(reverse=True)
            image_list = [src[offset[0]:offset[1], :] for offset in offset_list]
            return image_list
    
    def left2right(self, dst, image_num):
        pass
    
    def right2left(self, dst, image_num):
        pass
    
    def enlarge(self):
        "放大图片效果"
        pass
    
    def shrink(self):
        "缩小图片效果"
        pass
    
    def save_video(self):
        pass
    
    def test(self):
        videowrite = cv2.VideoWriter("mytest.mp4", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, self.video_resolution)
        for image in self.image_list:
            for _ in range(10):
                videowrite.write(image)
    
     
if __name__ == '__main__':
    co = ImageConvert2Video(r"C:\Users\YU\Desktop\image", (500, 760), 30, "",r"mytest.avi")
    videowrite = cv2.VideoWriter(r"mytest-60.avi", cv2.VideoWriter_fourcc(*'MJPG'), 30, (760, 500))
    for image in co.image_list:
        image_list = co.down2up(image, 30, (image.shape[0],500))
        for image in image_list:
            image = cv2.resize(image, dsize=(760, 500))
            videowrite.write(image)
    videowrite.release()
    # for image in co.image_list:
    #     cv2.imshow("123", image)
    #     cv2.waitKey()
