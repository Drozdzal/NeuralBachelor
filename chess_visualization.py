import chess
import chess.svg
from time import sleep
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

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



# chessboard=ChessVisualizer()
# app = QApplication([])
# window = MainWindow()
#
# while True:
#         try:
#             piece=input('wpisz pionek')
#             pole=input('wpisz pole')
#             chessboard.set_piece_on_field(piece,pole)
#             board=chessboard.actualize_board()
#             window.set_board(board)
#             window.show()
#         except Exception as e:
#             print(f"Error with piece type again {e}")
#         app.exec()
#         sleep(1)

