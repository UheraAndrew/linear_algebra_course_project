from time import time as now

import cv2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from config import max_players_number
from twod_transform import transform
from yolo_player_detect import detect


__players1 = []
__players2 = []


def dist_between_centroids(one, two):
    return (one[0] - two[0]) ** 2 + (one[1] - two[1]) ** 2


def _inside_field_v2(box, field_coords):
    x, y, w, h = box
    point = Point(x + (w // 2), y + h)
    polygon = Polygon(field_coords)
    return polygon.contains(point)


def __update(in_data, field_width, field_height):
    x, y, field = in_data
    y_n = None
    x_n = None
    if field == "L":
        y_n = (1 - y) * field_height
        x_n = (field_width // 2) * (1 - x)
    else:
        y_n = (1 - y) * field_height
        if y_n < 0:
            y_n = field_height + y_n * 2
        x_n = (field_width // 2) + x * (field_width // 2)
    return [x_n, y_n]


def update_players_coordinates(old_boxes, new_boxes):
    for i in range(len(old_boxes)):
        closest = None
        closest_dist = None
        one = (old_boxes[i][0] + old_boxes[i][2] // 2, old_boxes[i][1] + old_boxes[i][3])
        for j in range(len(new_boxes)):
            if new_boxes[j] is None: continue
            two = (new_boxes[j][0] + new_boxes[j][2] // 2, new_boxes[j][1] + new_boxes[j][3])
            dist = dist_between_centroids(one, two)
            if closest is None:
                closest = j
                closest_dist = dist
            else:
                if closest_dist > dist:
                    closest = j
                    closest_dist = dist
        if closest is not None:
            old_boxes[i] = new_boxes[closest]
            new_boxes[closest] = None
    update_time = now()
    for i in range(len(old_boxes)):
        if update_time - old_boxes[i][-1] > 3:
            old_boxes[i] = None
    while None in old_boxes:
        i = old_boxes.index(None)
        del old_boxes[i]
    for i in new_boxes:
        if i is not None and len(__players1) + len(__players2) < max_players_number:
            old_boxes.append(i)


def find__players(frame1, field_cords1, frame2, field_cords2):
    players1 = detect(frame1)
    players2 = detect(frame2)

    players1 = list(filter(lambda x: _inside_field_v2(x, field_cords1), players1))
    players2 = list(filter(lambda x: _inside_field_v2(x, field_cords2), players2))
    for i in range(len(players1)):
        players1[i].append(now())

    for i in range(len(players2)):
        players2[i].append(now())

    if len(__players1) == 0:
        __players1.extend(players1)
    else:
        update_players_coordinates(__players1, players1)

    if len(__players2) == 0:
        __players2.extend(players2)
    else:
        update_players_coordinates(__players2, players2)

    for i in __players1:
        x, y, w, h, t = i
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 3)
    for i in __players2:
        x, y, w, h, t = i
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 3)

    number_of_detected_players = len(__players1) + len(__players2)
    return number_of_detected_players


def render_2d_field(img, field1, field2):
    # len(field[0]) == width
    # len(field) == height
    for i in __players1:
        cor = [i[0] + i[2] // 2, i[1] + i[3]]
        i_c = transform(cor, field1, 0)
        i_u = __update(i_c + ["L"], len(img[0]), len(img))
        x, y = i_u
        x, y = round(x), round(y)
        cv2.rectangle(img, (x, y), (x + 25, y + 25), (255, 0, 0), 4)
    for i in __players2:
        cor = [i[0] + i[2] // 2, i[1] + i[3]]
        i_c = transform(cor, field2, 1)
        i_u = __update(i_c + ["R"], len(img[0]), len(img))
        x, y = i_u
        x, y = round(x), round(y)
        cv2.rectangle(img, (x, y), (x + 25, y + 25), (255, 0, 0), 4)