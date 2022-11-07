from chessboard_detectors import ChessboardDetector
from chess_visualization import ChessVisualizer
import chess

class ChessSystem:
    def __init__(self):
        self.chessboard_detector=ChessboardDetector()
        self.board = chess.Board()
        self.chessboard=ChessVisualizer()



    def update_board(self):
        piece='black-pawn'
        pole='A5'
        self.chessboard.set_piece_on_field(piece,pole)
        self.chessboard.actualize_board()
        while 1:
            piece=input("Wpiisz piece")
            pole=input('Wpisz pole')
            self.chessboard.set_piece_on_field(piece,pole)
            self.chessboard.actualize_board()