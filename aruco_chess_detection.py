import cv2
import cv2.aruco as aruco
import numpy as np
import time
from matplotlib import pyplot as plt
import math
import chess
from chessboard import display
from time import sleep

class ChessVisualizer:
    def __init__(self):
        self.chessboard=display.start()
        self.board=chess.Board()
        self.board.clear_board()
        self.actualize_board()
        self.colors={'black':chess.BLACK,
                     'white':chess.WHITE}
        self.pieces={'pawn':chess.PAWN,
                     'king':chess.KING,
                     'queen':chess.QUEEN,
                     'knight':chess.KNIGHT,
                     'bishop':chess.BISHOP,
                     'rook':chess.ROOK
                     }
        self.squares={'A1':chess.A1,
                      'B1':chess.B1,
                      'C1':chess.C1,
                      'D1':chess.D1,
                      'E1':chess.E1,
                      'F1':chess.F1,
                      'G1':chess.G1,
                      'H1':chess.H1,
                      'A2':chess.A2,
                      'B2':chess.B2,
                      'C2':chess.C2,
                      'D2':chess.D2,
                      'E2':chess.E2,
                      'F2':chess.F2,
                      'G2':chess.G2,
                      'H2':chess.H2,
                      'A3':chess.A3,
                      'B3':chess.B3,
                      'C3':chess.C3,
                      'D3':chess.D3,
                      'E3':chess.E3,
                      'F3':chess.F3,
                      'G3':chess.G3,
                      'H3':chess.H3,
                      'A4':chess.A4,
                      'B4':chess.B4,
                      'C4':chess.C4,
                      'D4':chess.D4,
                      'E4':chess.E4,
                      'F4':chess.F4,
                      'G4':chess.G4,
                      'H4':chess.H4,
                      'A5':chess.A5,
                      'B5':chess.B5,
                      'C5':chess.C5,
                      'D5':chess.D5,
                      'E5':chess.E5,
                      'F5':chess.F5,
                      'G5':chess.G5,
                      'H5':chess.H5,
                      'A6':chess.A6,
                      'B6':chess.B6,
                      'C6':chess.C6,
                      'D6':chess.D6,
                      'E6':chess.E6,
                      'F6':chess.F6,
                      'G6':chess.G6,
                      'H6':chess.H6,
                      'A7':chess.A7,
                      'B7':chess.B7,
                      'C7':chess.C7,
                      'D7':chess.D7,
                      'E7':chess.E7,
                      'F7':chess.F7,
                      'G7':chess.G7,
                      'H7':chess.H7,
                      'A8':chess.A8,
                      'B8':chess.B8,
                      'C8':chess.C8,
                      'D8':chess.D8,
                      'E8':chess.E8,
                      'F8':chess.F8,
                      'G8':chess.G8,
                      'H8':chess.H8}

    def actualize_board(self):
        try:
            display.update(self.board.fen(),self.chessboard)
        except Exception as e:
            print(f"Couldnt actualize display \n {e}")

    def set_piece_on_field(self,network_piece,chess_position):
        piece=self.transform_piece(network_piece)
        chess_square=self.transform_position(chess_position)
        self.board.set_piece_at(chess_square,piece)

    def transform_position(self,chess_position):
        chess_square=self.squares[chess_position]
        return chess_square

    def transform_piece(self,network_piece):
        color=network_piece.split("-")[0]
        color=self.colors[color]
        name_of_piece=network_piece.split("-")[1]
        name_of_piece=self.pieces[name_of_piece]
        #TODO:
        piece=chess.Piece(name_of_piece,color)
        return piece

    def __del__(self):
        display.terminate()


class Chessboard_Vision:
    def __init__(self):
        self.M=np.eye(3)

    def set_image(self,image):
        self.image=image

    def change_perspective(self, points):
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
        self.M=M
        out = cv2.warpPerspective(self.image, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        self.transformed_image=out

    def get_M_matrix(self):
        print(self.M)

    def calculate_aruco(self):
        MARKER_SIZE = 20
        ARUCO_ID = 0
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        parameters = aruco.DetectorParameters_create()
        marker_size = 20

        corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(self.image.copy(), corners, ids)
        aruco_corners_list = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

        for iterator in range(len(corners[0][0])):
            one_corner = corners[0][0][iterator]
            aruco_corners_list.append([int(one_corner[0]), int(one_corner[1])])

        chessboard_corners = self.aruco_chessboard_corditates(aruco_corners_list)


        self.change_perspective( chessboard_corners)
        cv2.imwrite('transfered_image.jpg',self.transformed_image)



    def aruco_chessboard_corditates(self,aruco_corners_list):
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

    def create_pieces_dict(self,txt_file):
        figures_dictionary = {'1': 'black-queen',
                              '2': 'black-king',
                              '3': 'black-pawn',
                              '4': 'black-knight',
                              '5': 'black-bishop',
                              '6': 'black-rook',
                              '7': 'white-queen',
                              '8': 'white-king',
                              '9': 'white-pawn',
                              '10': 'white-knight',
                              '11': 'white-bishop',
                              '12': 'white-rook'
                              }
        pieces_dictionary={}
        image_height, image_width, _ = self.image.shape
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
        self.pieces_dictionary=pieces_dictionary

    def create_grid_dict(self):

        width,height,_=self.transformed_image.shape
        print(f'width {width}')
        single_height=height/8
        single_width=width/8
        grid_dict={}
        for i,position in enumerate(['A','B','C','D','E','F','G','H']):
            for j in [1,2,3,4,5,6,7,8]:
                grid_dict.update({f'{position}{j}':[f'{position}{j}',single_height*(0.5+i),single_width*(0.5+j),single_height,single_width]})
        self.grid_dict=grid_dict

    def print_dict(self,dict):
                for item in dict:
                    label, x, y, w, h = dict[item]
                    x=float(x)
                    y=float(y)
                    w=float(w)
                    h=float(h)
                    upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
                    lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
                    cv2.rectangle(self.transformed_image,upper_right_corner,lower_left_corner,(0,255,0), 3)
                cv2.imwrite('result.jpg',self.transformed_image)
                cv2.waitKey()

    def get_pieces_dict(self):
        print(self.pieces_dictionary)

    def get_grid_dict(self):
       print(self.grid_dict)

    def transform_pieces(self):
        for piece in self.pieces_dictionary:
            label,x,y,width,height=self.pieces_dictionary[piece]
            position=np.array((x,y,1))
            x,y,z=np.dot(self.M,position)
            self.pieces_dictionary[piece]=[label,x,y,width,height]

    def print_grid(self):
        self.print_dict(self.grid_dict)

    def print_pieces(self):
        self.print_dict(self.pieces_dictionary)

    def calculate_piece_position(self):
        self.result={}
        for i,piece in enumerate(self.pieces_dictionary):
            lowest_val=10000000000
            piece_label,piece_x,piece_y,piece_width,piece_height=self.pieces_dictionary[piece]
            for position in self.grid_dict:
                position_label,position_x,position_y,position_width,position_height=self.grid_dict[position]
                mean_square_error=math.sqrt(math.pow(position_x-piece_x,2)+math.pow(position_y-piece_y,2))
                print(f'mean_square={mean_square_error}')
                if mean_square_error<lowest_val:
                    lowest_val=mean_square_error
                    piece_position=position
            self.result.update({i:[piece_label,piece_position]})
            print(self.result)

    def get_result(self):
        return self.result
if __name__ == "__main__":
    image = cv2.imread('obraz.jpg')
    machine=Chessboard_Vision()
    machine.set_image(image)
    machine.calculate_aruco()
    machine.create_pieces_dict('obraz.txt')
    machine.create_grid_dict()
    machine.get_pieces_dict()
    machine.get_grid_dict()
    machine.get_M_matrix()
    machine.transform_pieces()
    machine.print_grid()
    machine.print_pieces()
    machine.calculate_piece_position()
    result=machine.get_result()
    board = chess.Board()
    chessboard=ChessVisualizer()
    while True:
        try:
            input("Czy dokonac zmian?")
            for i in result:
                piece=result[i][0]
                pole=result[i][1]
                chessboard.set_piece_on_field(piece,pole)
                chessboard.actualize_board()
        except Exception as e:
            print(f"Error with piece type again {e}")
        sleep(1)
    #print_dict(image,pieces_dict)


