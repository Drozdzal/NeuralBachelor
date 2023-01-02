import cv2

src=cv2.imread('detect.jpg')
scale_percent=300
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)

# resize image
output = cv2.resize(src, dsize)
cv2.imwrite('nowy_2.jpg',output)