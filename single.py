import cv2
import numpy as np
from matplotlib import pyplot as plt
from copy import copy
from numpy import ma
def with_canny():
    img = cv2.imread('testo.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,160,200)
    gray = np.float32(gray)

    #edges = cv2.cornerHarris(gray,10,5,0.01)
    # najwazniejsze
    lines = cv2.HoughLines(edges,0.5,np.pi/180,20)
    for rho,theta in lines[:,0]:
        plt.plot(rho, theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.imwrite('houghlines4.jpg',edges)
    cv2.imwrite('houghlines3.jpg',img)

def with_harris():
    img = cv2.imread('testo.jpg')
    imgv2=copy(img)
    #img_blurred = cv2.GaussianBlur(img, (17, 17), 2)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel=(15,15)
    #gray = cv2.dilate(gray, kernel, iterations=10)
    #gray= cv2.erode(gray, kernel, iterations=5)

    gray = np.float32(gray)
    height,width,_=img.shape
    blank_image = np.zeros((height, width, 1), np.uint8)
    #blank_image = np.zeros((height, width, 3), np.float32)+
    blank_image_v2 = np.zeros((height, width, 1), np.uint8)

    dst = cv2.cornerHarris(gray,1,1,-1)
    #dst=cv2.GaussianBlur(dst, (31, 31), 5)
    #(szary_obraz, ,kernel,
    blank_image[dst > 0.01 * dst.max()] = 255
    edges=blank_image
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    #(edges, rho,pi,points?)
    print(f'type={type(edges)} size={edges.shape}')
    #linesv2=np.array((lines[:,0,0],lines[:,0,1],1))
    #print(f'type={type(linesv2)} size={linesv2.shape}')
    #print(f'max rho= {lines[:,0,0].}')
    rho_list=np.array([])
    theta_list=np.array([])
    try:
        for rho,theta in lines[:,0]:
            rho_list=np.append(rho_list,int(rho))
            theta_list=np.append(theta_list,int(theta))
            # plt.plot(int(theta),int(rho),'*')
            # #print(f"rho={rho},theta={theta}")
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a*rho
            # y0 = b*rho
            # cv2.drawMarker(imgv2, (int(x0), int(y0)), color=(0,255,0), markerType=cv2.MARKER_CROSS, thickness=2)
            # length=5000
            # x1 = int(x0 + length*(-b))
            # y1 = int(y0 + length*(a))
            # x2 = int(x0 - length*(-b))
            # y2 = int(y0 - length*(a))
            # cv2.drawMarker(imgv2, (int(x2), int(y2)), color=(255, 0, 0), markerType=cv2.MARKER_CROSS, thickness=2)
            # cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
    except Exception as e:
        print(f"{e}")
    print(f'rho_list={rho_list}')
    print(f'theta_list={theta_list}')
    value,numbers=np.unique(theta_list,return_counts=True)
    print(np.unique(theta_list,return_counts=True))
    vertical=np.where(theta_list==1)[0]
    horizontal=np.where(theta_list == 3)[0]
    try:
        for i in vertical:
            rho,theta=lines[i,0]
            rho_list=np.append(rho_list,int(rho))
            theta_list=np.append(theta_list,int(theta))
            plt.plot(int(theta),int(rho),'*')
            #print(f"rho={rho},theta={theta}")
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            cv2.drawMarker(imgv2, (int(x0), int(y0)), color=(0,255,0), markerType=cv2.MARKER_CROSS, thickness=2)
            length=5000
            x1 = int(x0 + length*(-b))
            y1 = int(y0 + length*(a))
            x2 = int(x0 - length*(-b))
            y2 = int(y0 - length*(a))
            cv2.drawMarker(imgv2, (int(x2), int(y2)), color=(255, 0, 0), markerType=cv2.MARKER_CROSS, thickness=2)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
    except Exception as e:
        print(f"{e}")

    try:
        for i in horizontal:
            rho,theta=lines[i,0]
            rho_list=np.append(rho_list,int(rho))
            theta_list=np.append(theta_list,int(theta))
            plt.plot(int(theta),int(rho),'*')
            #print(f"rho={rho},theta={theta}")
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            cv2.drawMarker(imgv2, (int(x0), int(y0)), color=(0,255,0), markerType=cv2.MARKER_CROSS, thickness=2)
            length=5000
            x1 = int(x0 + length*(-b))
            y1 = int(y0 + length*(a))
            x2 = int(x0 - length*(-b))
            y2 = int(y0 - length*(a))
            cv2.drawMarker(imgv2, (int(x2), int(y2)), color=(255, 0, 0), markerType=cv2.MARKER_CROSS, thickness=2)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
    except Exception as e:
        print(f"{e}")
    #print(ma.masked_where(theta_list, 2.0))


    cv2.imwrite('houghlines4.jpg',edges)
    cv2.imwrite('houghlines3.jpg',img)
    cv2.imwrite('after_1st_hough.jpg',imgv2)
    plt.show()

def algorithm():
    img=cv2.imread('testo.jpg')
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.jpg',gray)
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)
    print(corners)

#algorithm()
#with_canny()
with_harris()
