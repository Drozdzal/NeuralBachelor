from chessboard_detectors import ChessboardDetector
from chess_visualization import ChessVisualizer
from chess_visualization import MainWindow
from pieces_detectors import PiecesDetector
import chess
import cv2
import numpy as np

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
        self.chessboard_detector.print_dictionary('chessboard.jpg')
        self.pieces_detector.print_dictionary('pieces.jpg')

    def change_perspective(self):
        point_A = self.chessboard_detector.dictionary['marker_0']
        point_A = np.array(point_A[1:3])
        point_B = self.chessboard_detector.dictionary['marker_1']
        point_B = np.array(point_B[1:3])
        point_C = self.chessboard_detector.dictionary['marker_2']
        point_C = np.array(point_C[1:3])
        point_D = self.chessboard_detector.dictionary['marker_3']
        point_D = np.array(point_D[1:3])

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
        cv2.imwrite('transformed_image.jpg',out)

chess=ChessSystem()
image=cv2.imread('testo.jpg')
chess.set_image(image)
chess.single_detection()
chess.change_perspective()