from chessboard_detectors import ChessboardDetector
from chess_visualization import ChessVisualizer
from chess_visualization import MainWindow
from pieces_detectors import PiecesDetector
import chess
import cv2
import numpy as np
import math
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from time import sleep
class ChessSystem:
    def __init__(self):
        self.chessboard_detector=ChessboardDetector('multiple_aruco')
        self.pieces_detector=PiecesDetector('yolo')
        self.chessboard=ChessVisualizer()


    def set_image(self,image):
        self.image=image
        self.chessboard_detector.set_image(image)
        self.pieces_detector.set_image(image)

    def single_detection(self):
        self.chessboard_detector.detect()
        self.pieces_detector.detect()
        print(f'Chessboard {self.chessboard_detector.dictionary}')
        print(f'Pieces {self.pieces_detector.dictionary}')
        self.print_all_dics()

    def print_all_dics(self):
        self.chessboard_detector.print_dictionary('chessboard.jpg')
        self.pieces_detector.print_dictionary('pieces.jpg')
    def change_perspective(self):

        point_A = self.chessboard_detector.dictionary['marker_2']
        print(f'Point A {point_A}')
        point_A = np.array(point_A[1:3])
        point_B = self.chessboard_detector.dictionary['marker_1']
        print(f'Point B {point_B}')
        point_B = np.array(point_B[1:3])
        point_C = self.chessboard_detector.dictionary['marker_3']
        print(f'Point C {point_C}')
        point_C = np.array(point_C[1:3])
        point_D = self.chessboard_detector.dictionary['marker_0']
        print(f'Point D {point_D}')
        point_D = np.array(point_D[1:3])

        # #TODO: zmienic change perspective bo sie sypie
        # point_A = self.chessboard_detector.dictionary['marker_2']
        # print(f'Point A {point_A}')
        # point_A = np.array(point_A[1:3])
        # point_B = self.chessboard_detector.dictionary['marker_3']
        # print(f'Point B {point_B}')
        # point_B = np.array(point_B[1:3])
        # point_C = self.chessboard_detector.dictionary['marker_1']
        # print(f'Point C {point_C}')
        # point_C = np.array(point_C[1:3])
        # point_D = self.chessboard_detector.dictionary['marker_0']
        # print(f'Point D {point_D}')
        # point_D = np.array(point_D[1:3])

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
        self.transformed_image = cv2.warpPerspective(self.image, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        cv2.imwrite('transformed_image.jpg',self.transformed_image)

        self.transformed_pieces=self.pieces_detector.dictionary

        for piece in self.transformed_pieces:
            label,x,y,width,height=self.transformed_pieces[piece]
            position=np.array((x,y,1))
            x,y,z=np.dot(M,position)
            self.transformed_pieces[piece]=[label,x,y,width,height]
            self.transformed_image = cv2.warpPerspective(self.image, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

    def create_grid_dict(self):

        width, height, _ = self.transformed_image.shape
        print(f'width {width}')
        single_height = height / 8
        single_width = width / 8
        grid_dict = {}
        for i, position in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            for j in [1, 2, 3, 4, 5, 6, 7, 8]:
                grid_dict.update({f'{position}{j}': [f'{position}{j}', single_height * (0.5 + i),
                                                     single_width * (-0.5 + j), single_height, single_width]})
        self.grid_dict = grid_dict
    def print_transformed_pieces(self):
            if self.transformed_pieces:
                for item in self.transformed_pieces:
                    label, x, y, w, h = self.transformed_pieces[item]
                    x = float(x)
                    y = float(y)
                    w = float(w)
                    h = float(h)
                    upper_right_corner = (int(x + 0.5 * w), int(y + 0.5 * h))
                    lower_left_corner = (int(x - 0.5 * w), int(y - 0.5 * h))
                    cv2.rectangle(self.transformed_image, upper_right_corner, lower_left_corner, (0, 255, 0), 3)
                cv2.imwrite('whole_transformed_image.jpg',self.transformed_image)
            else:
                print("Dictionary not set")

    def print_grid(self):
                for item in self.grid_dict:
                    label, x, y, w, h = self.grid_dict[item]
                    x=float(x)
                    y=float(y)
                    w=float(w)
                    h=float(h)
                    upper_right_corner=(int(x+0.5*w),int(y+0.5*h))
                    lower_left_corner=(int(x-0.5*w),int(y-0.5*h))
                    cv2.rectangle(self.transformed_image,upper_right_corner,lower_left_corner,(0,255,0), 3)
                    cv2.putText(self.transformed_image, label, (int(x-50),int(y)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 1)
                print(f'Grid {self.grid_dict}')
                cv2.imwrite('with_grid.jpg',self.transformed_image)

    def calculate_piece_position(self):
        self.result={}
        for i,piece in enumerate(self.pieces_detector.dictionary):
            lowest_val=10000000000
            piece_label,piece_x,piece_y,piece_width,piece_height=self.pieces_detector.dictionary[piece]
            for position in self.grid_dict:
                position_label,position_x,position_y,position_width,position_height=self.grid_dict[position]
                mean_square_error=math.sqrt(math.pow(position_x-piece_x,2)+math.pow(position_y-piece_y,2))
                if mean_square_error<lowest_val:
                    lowest_val=mean_square_error
                    piece_position=position
            self.result.update({i:[piece_label,piece_position]})
        return self.result

    def from_id_to_piece(self,id:str):
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
        return figures_dictionary[id]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
    def set_board(self,board):
            self.setGeometry(100, 100, 1100, 1100)

            self.widgetSvg = QSvgWidget(parent=self)
            self.widgetSvg.setGeometry(10, 10, 1080, 1080)

            self.chessboard = board
            print(board)

            self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)

class ChessVisualizer:
    def __init__(self):

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
            return self.board
            print("actualie")
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
        #display.terminate()
        pass



chessboard=ChessVisualizer()

working_system=ChessSystem()
image=cv2.imread('nat_2.jpg')
working_system.set_image(image)
working_system.single_detection()
working_system.change_perspective()
working_system.print_transformed_pieces()
working_system.create_grid_dict()
working_system.print_grid()
results=working_system.calculate_piece_position()
app = QApplication([])
window = MainWindow()

while True:
            for result in results:
                try:
                    piece=working_system.from_id_to_piece(results[result][0])
                    print(f'Piece {piece}')
                    pole=results[result][1]
                    print(f'Pole {pole}')
                    chessboard.set_piece_on_field(piece,pole)
                except Exception as e:
                    print(f"PIECE_ERROR: {e}")
            board=chessboard.actualize_board()
            window.set_board(board)
            window.show()
            app.exec()
            sleep(1)