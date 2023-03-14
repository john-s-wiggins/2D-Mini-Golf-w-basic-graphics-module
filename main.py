from graphics import *
import time
import math

def calculate_hypotenuse(deltaX, deltaY):
    hypotenuse = math.sqrt(abs(deltaX) ** 2 + abs(deltaY) ** 2)
    return hypotenuse

def find_missing_side_length(side, hypotenuse):
    return math.sqrt((hypotenuse ** 2) - (side ** 2))

def get_power(win):
    #Uses mouse click in power bar to get a ratio of maximum power
    power_ratio = 1
    power_condition = False
    click = win.getMouse()
    while power_condition == False:
        if click.getX() > 635 and click.getX() < 701:
            if click.getY() > 43 and click.getY() < 703:
                power_ratio = abs(((click.getY() - 43) - 660)) / 660
                power_condition = True
            else:
                print("Please click in the POWER box to select power on your shot.")
                click = win.getMouse()
        else:
            print("Please click in the POWER box to select power on your shot.")
            click = win.getMouse()
    return power_ratio

def move_the_ball(win, ball, distance, angle, Background, hole):
    total_distance_travelled = 0
    ball.undraw()
    starting_point = ball.getCenter()
    movement_point = ball.getCenter()
    hole_point = hole.getCenter()


    split_x_frequency = math.modf(1/math.cos(angle)) #[1] is whole number, [0] is the decimal
    split_y_frequency = math.modf(1/math.sin(angle))

    x_whole = abs(split_x_frequency[1])
    x_decimal = abs(split_x_frequency[0])
    y_whole = abs(split_y_frequency[1])
    y_decimal = abs(split_y_frequency[0])

    x_collision_cooldown = 0
    y_collision_cooldown = 0

    while(total_distance_travelled < distance):

        x_whole -= 1
        if x_whole == 0:
            x_decimal += abs(split_x_frequency[0])
            movement_point.move(abs(split_x_frequency[1]) / split_x_frequency[1], 0)

            x_whole = abs(split_x_frequency[1])
            if x_decimal >= 1:
                x_decimal -= 1
                x_whole += 1

        y_whole -= 1
        if y_whole == 0:
            y_decimal += abs(split_y_frequency[0])
            movement_point.move(0, abs(split_y_frequency[1]) / split_y_frequency[1])

            y_whole = abs(split_y_frequency[1])
            if y_decimal > 1:
                y_decimal -= 1
                y_whole += 1

        ball.undraw()
        ball = Circle(movement_point, 3)
        ball.setFill(color_rgb(255, 255, 255))
        ball.draw(win)
        time.sleep(0.005)

        total_distance_travelled = calculate_hypotenuse(movement_point.getX() - starting_point.getX(), movement_point.getY() - starting_point.getY())
        current_point_x = int(movement_point.getX())
        current_point_y = int(movement_point.getY())
        #hole_point = hole.getCenter()

        if current_point_x >= int(hole_point.getX()) - 6 and current_point_x <= int(hole_point.getX()) + 6:
            if current_point_y >= int(hole_point.getY()) - 6 and current_point_y <= int(hole_point.getY()) + 6:
                return [1, 0, 0]

        if total_distance_travelled >= distance:
            ball.undraw()
            return [0, current_point_x, current_point_y]

        x_collision_cooldown = x_collision_cooldown - 1
        y_collision_cooldown = y_collision_cooldown - 1

        if x_collision_cooldown <= 0:
            if Background.getPixel(current_point_x + 4, current_point_y) != [0, 0, 0] or Background.getPixel(
                    current_point_x - 4, current_point_y) != [0, 0, 0]:
                angle = math.pi - angle

                starting_point = ball.getCenter()
                movement_point = ball.getCenter()
                split_x_frequency = math.modf(1 / math.cos(angle))  # [1] is whole number, [0] is the decimal
                split_y_frequency = math.modf(1 / math.sin(angle))

                x_whole = abs(split_x_frequency[1])
                x_decimal = abs(split_x_frequency[0])
                y_whole = abs(split_y_frequency[1])
                y_decimal = abs(split_y_frequency[0])

                x_collision_cooldown = split_x_frequency[1] + 1
                distance = distance - total_distance_travelled

        if y_collision_cooldown <= 0:
            if Background.getPixel(current_point_x, current_point_y + 4) != [0, 0, 0] or Background.getPixel(
                    current_point_x, current_point_y - 4) != [0, 0, 0]:
                angle = 2 * math.pi - angle

                starting_point = ball.getCenter()
                movement_point = ball.getCenter()
                split_x_frequency = math.modf(1 / math.cos(angle))  # [1] is whole number, [0] is the decimal
                split_y_frequency = math.modf(1 / math.sin(angle))

                x_whole = abs(split_x_frequency[1])
                x_decimal = abs(split_x_frequency[0])
                y_whole = abs(split_y_frequency[1])
                y_decimal = abs(split_y_frequency[0])

                y_collision_cooldown = split_y_frequency[1] + 1
                distance = distance - total_distance_travelled

        ball.undraw()
        ball = Circle(movement_point, 3)
        ball.setFill(color_rgb(255, 255, 255))
        ball.draw(win)

        total_distance_travelled = calculate_hypotenuse(movement_point.getX() - starting_point.getX(), movement_point.getY() - starting_point.getY())


def hit_ball(win, ball, Background, hole):

    ball_results = [0, 0, 0]
    while ball_results[0] == 0:

        mouse_click = win.getMouse()
        ball_position = ball.getCenter()

        angle = get_angle(ball_position.getX(), ball_position.getY(), mouse_click.getX(), mouse_click.getY())
        distance = 1000 * get_power(win)

        ball.undraw()
        ball_results = move_the_ball(win, ball, distance, angle, Background, hole)
        if ball_results[0] == 1:
            pass

        ball = Circle(Point(ball_results[1], ball_results[2]), 3)
        ball.setFill(color_rgb(255, 255, 255))
        ball.draw(win)

def get_distance(origin, end):
    #arguments should be respective x and y values. such as pt1.x and pt2.x
    return abs(end - origin)

def get_angle(startX, startY, endX, endY):
    #returns angle in radians
    deltaY = endY - startY
    deltaX = endX - startX
    angle = math.atan2(deltaY, deltaX)
    return angle

def main():
    win = GraphWin("Game Window", 720, 720) #first argument: name of window, next two, creation of window
    win.setBackground(color_rgb(0, 0, 0)) #max value 255, min 0

    Background = Image((Point(360, 360)), "MiniGolfCourse1.gif")
    Background.draw(win)
    
    ball = Circle(Point(50, 50), 3)
    ball.setFill(color_rgb(255, 255, 255))
    ball.draw(win)

    hole = Circle(Point(525, 130), 6)
    hole.setFill(color_rgb(0, 255, 75))
    hole.draw(win)

    hit_ball(win, ball, Background, hole)
    
    ball.undraw()
    hole.undraw()
    Background.undraw()

    Background = Image((Point(360, 360)), "MiniGolfCourse2.gif")
    Background.draw(win)

    ball = Circle(Point(360, 325), 3)
    ball.setFill(color_rgb(255, 255, 255))
    ball.draw(win)

    hole = Circle(Point(190, 325), 6)
    hole.setFill(color_rgb(0, 255, 75))
    hole.draw(win)

    hit_ball(win, ball, Background, hole)

    ball.undraw()
    hole.undraw()
    Background.undraw()

    Background = Image((Point(360, 360)), "MiniGolfCourse3.gif")
    Background.draw(win)

    ball = Circle(Point(300, 330), 3)
    ball.setFill(color_rgb(255, 255, 255))
    ball.draw(win)

    hole = Circle(Point(500, 330), 6)
    hole.setFill(color_rgb(0, 255, 75))
    hole.draw(win)

    hit_ball(win, ball, Background, hole)

    win.close()

main()