from Base import BaseOperations
import cv2
import cv2.aruco as aruco
import numpy as np

class ChessboardDetector(BaseOperations):

    def single_aruco_detect(self):
        self.aruco_chessboard_corditates=[]
        self.find_aruco()
        self.chessboard_from_aruco()
        self.print_dictionary('aruco_detection.png')

    def multiple_aruco_detect(self):
        self.aruco_chessboard_corditates=[]
        self.find_multiple_aruco(id=0)
        self.print_dictionary('multiple_aruco_detection.png')

    def find_multiple_aruco(self,id):
        MARKER_SIZE = 20
        ARUCO_ID = id
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        parameters = aruco.DetectorParameters_create()
        marker_size = 20
        corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(self.image.copy(), corners, ids)
        aruco_corners_list = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
        for id in range(len(ids)):
            one_corner = corners[id][0][0]
            aruco_corners_list.append([int(one_corner[0]), int(one_corner[1])])
            corner_label=f'marker_{id}'
            self.dictionary.update({corner_label:[corner_label,int(one_corner[0]), int(one_corner[1]),5,5]})

    def find_aruco(self):
        MARKER_SIZE = 20
        ARUCO_ID = 0
        self.aruco_dict={}
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        parameters = aruco.DetectorParameters_create()
        marker_size = 20

        corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(self.image.copy(), corners, ids)
        aruco_corners_list = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

        for i in range(len(corners[0][0])):
            one_corner = corners[0][0][i]
            aruco_corners_list.append([int(one_corner[0]), int(one_corner[1])])
            corner_label=f'corner_{i}'
            self.aruco_dict.update({corner_label:[corner_label,int(one_corner[0]), int(one_corner[1]),5,5]})

        print(f'ARUCO_CORNERS:{self.aruco_dict}')

    def chessboard_from_aruco(self):
        scalar_aruco_to_chessboard = 21 / 4
        aruco_corners_list = self.aruco_dict
        chessboard_corners = []
        chessboard_A_point = aruco_corners_list['corner_1']
        _,x_A,y_A,_,_=chessboard_A_point
        _,x_W,y_W,_,_=aruco_corners_list['corner_2']
        _,x_H,y_H,_,_=aruco_corners_list['corner_0']
        self.dictionary.update({'chessboard_A':chessboard_A_point})
        width = np.array((x_W-x_A,y_W-y_A))
        height=np.array((x_H-x_A,y_H-y_A))
        chessboard_width_translation = width * scalar_aruco_to_chessboard
        chessboard_height_translation = height * scalar_aruco_to_chessboard
        chessboard_D_point = {'chessboard_D': ['chessboard_D',x_A - chessboard_height_translation[0],y_A - chessboard_height_translation[1],5,5]}
        chessboard_B_point = {'chessboard_B':['chessboard_B',x_A - chessboard_width_translation[0],y_A - chessboard_width_translation[1],5,5]}
        chessboard_C_point = {'chessboard_C':['chessboard_C',x_A - chessboard_width_translation[0] - chessboard_height_translation[0],y_A - chessboard_width_translation[1] - chessboard_height_translation[1],5,5]}
        self.dictionary.update(chessboard_B_point)
        self.dictionary.update(chessboard_C_point)
        self.dictionary.update(chessboard_D_point)
        print(self.dictionary)

    def print_aruco(self):
        self.print_points(self.aruco_dict)
        print('Aruco saved')

    def operators_detect(self):
        pass

    def cnn_detect(self):
        pass


image = cv2.imread('aruco4.png')
chessboard=machine=ChessboardDetector('multiple_aruco')
chessboard.set_image(image)
chessboard.detect()
