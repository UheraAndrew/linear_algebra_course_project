import cv2
import numpy as np

import player_frame
from config import left_field_side_video_path, right_field_side_video_path
from user_points_input import get_field_main_points

vid1 = cv2.VideoCapture(left_field_side_video_path)
vid2 = cv2.VideoCapture(right_field_side_video_path)

success1, image1 = vid1.read()
success2, image2 = vid2.read()

field_coords1 = get_field_main_points(image1, "Select four point of field")
field_coords2 = get_field_main_points(image2, "Select four point of field")

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
