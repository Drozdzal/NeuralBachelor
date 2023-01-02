from roboflow import Roboflow

rf = Roboflow(api_key="ITfau95DUAvhPhenbVvS")
project = rf.workspace("politechnika-warszawska").project("chess-bprbi")
dataset = project.version(3).download("yolov5")