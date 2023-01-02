import os
from Base import BaseOperations
import cv2
import time
import numpy as np
def funkcja():

    os.system(f'python3 yolov5/detect.py')
class PiecesDetector(BaseOperations):
    def yolo_detect(self):
        path_to_result='yolov5/runs/detect/result/labels/detecting_image.txt'
        cv2.imwrite('yolov5/detecting_image.jpg',self.image)
        try:
            os.remove(path_to_result)
        except Exception as e:
            print("Nie ma pliku do usuniecia")
        time.sleep(1)
        os.system(f'python3 yolov5/detect.py')
        time.sleep(2)
        image_height,image_width,_=self.image.shape
        with open(path_to_result, 'r') as figures:
            for i,line in enumerate(figures):
                print(f'figury= {line}')
                piece_label, x, y, w, h = line.split(' ')
                x = float(x)
                y = float(y)
                w = float(w)
                h = float(h)
                x *= image_width
                w *= image_width
                y *= image_height
                h *= image_height
                self.dictionary.update({i: [piece_label, int(x), int(y), int(w), int(h)]})
        print(f'Pieces dictionary {self.dictionary}')



    def change_dict_perspective(self,M):
        for piece in self.dictionary:
            label, x, y, width, height = self.dictionary[piece]
            position = np.array((x, y, 1))
            x, y, z = np.dot(M, position)
            self.dictionary[piece] = [label, x, y, width, height]

# image = cv2.imread('obraz.jpg')
# pieces=machine=PiecesDetector('yolo')
# pieces.set_image(image)
# pieces.detect()
# pieces.print_dictionary('pieces_detection.jpg')

