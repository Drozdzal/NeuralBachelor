from abc import ABC, abstractmethod
import cv2
import numpy as np

class BaseOperations(ABC):
    def __init__(self,choosen_method: str = None):
        self.dictionary={}
        self.image=None
        self.method=choosen_method

    def detect(self):
        try:
            choosen_function='self.'+self.method+"_detect()"
            return eval(choosen_function)
        except Exception as e:
            print(f"You've choosen wrong method {e}")

    def set_image(self,image = None):
        if type(image) is np.ndarray:
            self.image=image
        else:
            print("Image not set image should be np.array type")
    @property
    def check_image(self):
        if self.image:
            return self.image
        else:
            print("You didnt set up an image, please do it. (Use methon set_image)")
    @property
    def get_dictionary(self):
        if len(self.dictionary):
            return self.get_dictionary
        else:
            print("You've didnt create a dictionary please, use detect method")

    def print_dictionary(self,name_of_image):
        if self.dictionary:
            self.transformed_image=self.image.copy()
            for item in self.dictionary:
                label, x, y, w, h = self.dictionary[item]
                x=float(x)
                y=float(y)
                w=float(w)
                h=float(h)
                upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
                lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
                cv2.rectangle(self.transformed_image,upper_right_corner,lower_left_corner,(0,255,0), 3)
            cv2.imwrite(name_of_image,self.transformed_image)
        else:
            print("Dictionary not set")

    def print_points(self,points_dict):
        if points_dict:
            self.transformed_image=self.image.copy()
            for item in self.dictionary:
                label, x, y, w, h = points_dict[item]
                x=float(x)
                y=float(y)
                w=float(w)
                h=float(h)
                upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
                lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
                cv2.rectangle(self.transformed_image,upper_right_corner,lower_left_corner,(0,255,0), 3)
            cv2.imwrite('result.jpg',self.transformed_image)
        else:
            print("Dictionary not set")


# my=Test()
# my.set_image()
# print(my.check_image)
# my.get_dictionary

