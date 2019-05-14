import cv2
import player_frame
from user_points_input import get_field_main_points
import numpy as np
vid1 = cv2.VideoCapture("static/data/left.mp4")
vid2 = cv2.VideoCapture("static/data/right.mp4")
success1, image1 = vid1.read()
success2, image2 = vid2.read()

field_coords1 = get_field_main_points(image1, "Select four point of field")

field_coords2 = get_field_main_points(image2, "Select four point of field")

detected_players = 0
player_frame.max_players_number = 14

while success1 and success2:
    success1, image1 = vid1.read()
    success2, image2 = vid2.read()
    field = cv2.imread("field.png")
    player_frame.find__players(image1, field_coords1, image2, field_coords2)
    player_frame.render_2d_field(field, field_coords1, field_coords2)
    image1 = cv2.resize(image1, (700, 500))
    image2 = cv2.resize(image2, (700, 500))
    whole_field = np.hstack((image1, image2))

    field = cv2.resize(field, (800, 500))

    cv2.imshow("Field", whole_field)
    cv2.imshow("Detection: ", field)
    cv2.waitKey(1)

vid1.release()
vid2.release()

