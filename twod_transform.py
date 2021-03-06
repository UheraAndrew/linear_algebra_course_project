import math

dot = lambda x, y: x[0] * y[0] + x[1] * y[1]

norm = lambda x: math.sqrt(sum(i ** 2 for i in x))

projection_koefficient = lambda base, up: dot(base, up) / (norm(base) ** 2)


def transform(player_coord, field_cords, side):
    if not side:
        up_down = list(sorted(field_cords, key=lambda y: y[1]))
        right_up = list(sorted(up_down[:2], key=lambda x: x[0]))[1]
        left_down, right_down = list(sorted(up_down[-2:], key=lambda x: x[0]))
        right_up = [abs(right_up[0] - right_down[0]), abs(right_up[1] - right_down[1])]
        left_down = [abs(left_down[0] - right_down[0]), abs(left_down[1] - right_down[1])]
        player = [abs(player_coord[0] - right_down[0]), abs(player_coord[1] - right_down[1])]
        proj_k = projection_koefficient(left_down, right_up)
        right_up = [right_up[0] - left_down[0] * proj_k,
                    right_up[1] - left_down[1] * proj_k]
        x_k = projection_koefficient(left_down, player)
        y_k = projection_koefficient(right_up, player)
        return [x_k, y_k]
    else:
        up_down = list(sorted(field_cords, key=lambda y: y[1]))
        left_up = list(sorted(up_down[:2], key=lambda x: x[0]))[0]
        left_down, right_down = list(sorted(up_down[-2:], key=lambda x: x[0]))
        left_up = [abs(left_up[0] - left_down[0]), abs(left_up[1] - left_down[1])]
        right_down = [abs(right_down[0] - left_down[0]), abs(right_down[1] - left_down[1])]
        player = [abs(player_coord[0] - left_down[0]), abs(player_coord[1] - left_down[1])]
        proj_k = projection_koefficient(right_down, left_up)
        left_up = [left_up[0] - proj_k * right_down[0], left_up[1] - proj_k * right_down[1]]
        x_k = projection_koefficient(right_down, player)
        y_k = projection_koefficient(left_up, player)
        return [x_k, y_k]