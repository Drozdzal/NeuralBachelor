import cv2

def print_piecces(img):
    result=open('test_szachy.txt')
    print(f'image shape = {img.shape}')
    image_height,image_width,_=img.shape
    with open('test_szachy.txt', 'r') as figures:
        for count, line in enumerate(figures):
            label,x,y,w,h=line.split(' ')
            x=float(x)
            y=float(y)
            w=float(w)
            h=float(h)
            x*=image_width
            w*=image_width
            y*=image_height
            h*=image_height
            print(f'X={x} type={type(x)}')
            upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
            lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
            cv2.rectangle(img,upper_right_corner,lower_left_corner,(0,255,0), 3)
            print(x)
            print('co jest')
    return img

img=cv2.imread('test_szachy.png')
img=print_piecces(img)
cv2.imshow('okienko',img)
cv2.waitKey()