import cv2
import cv2.aruco as aruco
import numpy as np
import time
from matplotlib import pyplot as plt
def change_perspective(image,points):
    # Here, I have used L2 norm. You can use L1 also.
    point_A=points[0]
    point_B=points[1]
    point_C=points[2]
    point_D=points[3]
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

    M = cv2.getPerspectiveTransform(input_pts,output_pts)
    out = cv2.warpPerspective(image,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
    return out


def calculate_aruco(cv_image):
    MARKER_SIZE=20
    ARUCO_ID=0

    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    camera_matrix = np.loadtxt('cameraMatrix_raspi.txt', delimiter=',')
    camera_distortion = np.loadtxt('cameraDistortion_raspi.txt', delimiter=',')
    # -- Find all the aruco markers in the image
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()
    marker_size=20
    

    # corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,                                       #cameraMatrix=camera_matrix, #distCoeff=camera_distortion)
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(cv_image.copy(), corners, ids)
    corners_list=[]
    for iterator in range(len(corners[0][0])):
        one_corner=corners[0][0][iterator]
        #cv2.drawMarker(cv_image,(int(one_corner[0]),int(one_corner[1])),color=(255,0,0), markerSize=5)
        corners_list.append([int(one_corner[0]),int(one_corner[1])])
    print(corners)
    out=change_perspective(image,corners_list)
    cv2.imshow('okno',out)
    cv2.waitKey()



if __name__ == "__main__":
    image=cv2.imread('2.jpg')
    responce=calculate_aruco(image)
    #cv2.drawMarker(image,(1586,885),color=(255,0,0), markerSize=5)


