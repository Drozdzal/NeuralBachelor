import os
from Base import BaseOperations
import cv2
import time
def funkcja():

    os.system(f'python3 yolov5/detect.py')
class PiecesDetector(BaseOperations):
    def yolo_detect(self):
        cv2.imwrite('yolov5/detecting_image.jpg',self.image)
        time.sleep(1)
        os.system(f'python3 yolov5/detect.py')
        path_to_result='yolov5/runs/detect/result/labels/detecting_image.txt'
        image_height,image_width,_=self.image.shape
        with open(path_to_result, 'r') as figures:
            for count, line in enumerate(figures):
                piece_label, x, y, w, h = line.split(' ')
                x = float(x)
                y = float(y)
                w = float(w)
                h = float(h)
                x *= image_width
                w *= image_width
                y *= image_height
                h *= image_height
                self.dictionary.update({piece_label: [piece_label, int(x), int(y), int(w), int(h)]})
        print(self.dictionary)

# image = cv2.imread('obraz.jpg')
# pieces=machine=PiecesDetector('yolo')
# pieces.set_image(image)
# pieces.detect()
# pieces.print_dictionary('pieces_detection.jpg')

