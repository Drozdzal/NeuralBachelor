import cv2
import cv2.aruco as aruco
import numpy as np
import time
from matplotlib import pyplot as plt


def change_perspective(image, points):
    # Here, I have used L2 norm. You can use L1 also.
    point_A = points[0]
    point_B = points[1]
    point_C = points[2]
    point_D = points[3]
    width_AD = np.sqrt(((point_A[0] - point_D[0]) ** 2) + ((point_A[1] - point_D[1]) ** 2))
    width_BC = np.sqrt(((point_B[0] - point_C[0]) ** 2) + ((point_B[1] - point_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((point_A[0] - point_B[0]) ** 2) + ((point_A[1] - point_B[1]) ** 2))
    height_CD = np.sqrt(((point_C[0] - point_D[0]) ** 2) + ((point_C[1] - point_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))
    input_pts = np.float32([point_A, point_B, point_C, point_D])
    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])

    M = cv2.getPerspectiveTransform(input_pts, output_pts)
    out = cv2.warpPerspective(image, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    return out


def calculate_aruco(cv_image):
    MARKER_SIZE = 20
    ARUCO_ID = 0
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()
    marker_size = 20

    # corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,                                       #cameraMatrix=camera_matrix, #distCoeff=camera_distortion)
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(cv_image.copy(), corners, ids)
    aruco_corners_list = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

    for iterator in range(len(corners[0][0])):
        one_corner = corners[0][0][iterator]
        # cv2.drawMarker(cv_image,(int(one_corner[0]),int(one_corner[1])),color=colors[iterator], markerSize=30, thickness=5)
        aruco_corners_list.append([int(one_corner[0]), int(one_corner[1])])

    chessboard_corners = aruco_chessboard_corditates(aruco_corners_list)


    out = change_perspective(cv_image, chessboard_corners)
    cv2.imwrite('rezultat.jpg',out)
    cv2.imshow('okno', out)
    cv2.waitKey()


def aruco_chessboard_corditates(aruco_corners_list):
    scalar_aruco_to_chessboard = 21 / 4
    aruco_corners_list = np.array(aruco_corners_list)
    chessboard_corners = []
    chessboard_A_point = aruco_corners_list[1]
    chessboard_corners.append(chessboard_A_point)
    width = aruco_corners_list[2] - chessboard_A_point
    height = aruco_corners_list[0] - chessboard_A_point
    chessboard_width_translation = width * scalar_aruco_to_chessboard
    chessboard_height_translation = height * scalar_aruco_to_chessboard
    chessboard_D_point = chessboard_A_point - chessboard_height_translation
    chessboard_B_point = chessboard_A_point - chessboard_width_translation
    chessboard_C_point = chessboard_A_point - chessboard_width_translation - chessboard_height_translation
    chessboard_corners.append(chessboard_B_point)
    chessboard_corners.append(chessboard_C_point)
    chessboard_corners.append(chessboard_D_point)
    return chessboard_corners

def create_pieces_dict(img,txt_file):
    figures_dictionary = {'1': 'black pawn',
                          '2': 'black king',
                          '3': 'black queen',
                          '4': 'black knight',
                          '5': 'black bishop',
                          '6': 'black rook',
                          '7': 'white pawn',
                          '8': 'white king',
                          '9': 'white queen',
                          '10': 'white knight',
                          '11': 'white bishop',
                          '12': 'white rook'
                          }
    pieces_dictionary={}
    image_height, image_width, _ = img.shape
    with open(txt_file, 'r') as figures:
        for count, line in enumerate(figures):
            label,x,y,w,h=line.split(' ')
            x=float(x)
            y=float(y)
            w=float(w)
            h=float(h)
            x *= image_width
            w*=image_width
            y*=image_height
            h*=image_height
            piece_label=figures_dictionary[label]
            pieces_dictionary.update({f'piece_{count}': [piece_label,x, y, w, h]})
    return pieces_dictionary

def create_grid_dict(transformed_img):
    print(transformed_img.shape)
    width,height,_=transformed_img.shape
    print(f'width {width}')
    single_height=height/8
    single_width=width/8
    grid_dict={}
    for i,position in enumerate(['A','B','C','D','E','F','G','H']):
        for j in range(8):
            grid_dict.update({f'{position}{j}':[f'{position}{j}',single_height*(0.5+i),single_width*(0.5+j),single_height,single_width]})
    return grid_dict

def print_dict(img,dict):
            for item in dict:
                label, x, y, w, h = dict[item]
                x=float(x)
                y=float(y)
                w=float(w)
                h=float(h)
                upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
                lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
                cv2.rectangle(img,upper_right_corner,lower_left_corner,(0,255,0), 3)
            cv2.imwrite('result.jpg',img)
            cv2.waitKey()


if __name__ == "__main__":
    image = cv2.imread('obraz.jpg')
    #responce = calculate_aruco(image)
    # cv2.drawMarker(image,(1586,885),color=(255,0,0), markerSize=5)
    pieces_dict=create_pieces_dict(image,'obraz.txt')

    grid_dict=create_grid_dict(image)
    print_dict(image,pieces_dict)


