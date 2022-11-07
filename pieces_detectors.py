import os

def funkcja():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    path_to_yolov5=os.path.join(dir_path,'yolov5/detect.py')
    print(path_to_yolov5)
    os.system(f'python3 {path_to_yolov5} --weights best.pt --img 416 --conf 0.4 --hide-conf --save-txt --source obraz.jpg')

#if __name__ == "__main__":
funkcja()