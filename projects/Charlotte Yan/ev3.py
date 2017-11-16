
#Charlotte Yan
#LEGO 15
#ev3 part


import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import traceback
import math

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


print('--------------------------------')
print('Final project for Charlotte Yan')
print('--------------------------------')

class speed_mudifier(object):
    def __init__(self):
        self.speed = 300
        self.turn = 0

    def getSpeed(self):
        return self.speed

    def getTurn(self):
        return self.turn

    def setParameter(self, speed, turn):
        self.speed = int(speed)
        self.turn = int(turn)
        print(self.speed, self.turn)

def main():
    print('--------------------')
    print('Beacon Seeking')
    print('--------------------')

    s_mudi = speed_mudifier()
    mqtt_client = com.MqttClient(s_mudi)
    mqtt_client.connect_to_ev3()
    s_mudi.mqtt = mqtt_client

    robot = robo.Snatch3r()

    robot.seek_beacon()
    print("A",time.time())
    catch_the_beacon(robot)
    print("B", time.time())
    find_the_color(robot, s_mudi)
    print("c", time.time())
    put_down_the_beacon(robot)


def catch_the_beacon(robot):

    forward_speed = 300
    turn_speed = 100
    beacon_seaker=ev3.BeaconSeeker(channel=1)

    while not robot.touch_sensor.is_pressed:
        current_heading = beacon_seaker.heading # use the beacon_seeker heading
        current_distance = beacon_seaker.distance  # use the beacon_seeker distance
        if current_distance == -128:
            print("IR Remote not found. Distance is -128")
            robot.stop()
        else:
            if math.fabs(current_heading) < 2:
                if current_distance == 1:
                    robot.drive_inches(4.5, forward_speed)
                    robot.stop()
                    robot.arm_up()
                    print("Found the beacon!")
                    return True
                print("On the right heading. Distance: ", current_distance)
                if current_distance > 1:
                    robot.drive(forward_speed, forward_speed)
                    time.sleep(0.1)
            if 2 < math.fabs(current_heading) < 10:
                if current_heading > 0:
                    robot.drive(turn_speed, -turn_speed)
                    time.sleep(0.1)
                    print("Adjusting heading right: ", current_heading)

                if current_heading < 0:
                    robot.drive(-turn_speed, turn_speed)
                    time.sleep(0.1)
                    print("Adjusting heading left: ", current_heading)

            if math.fabs(current_heading) > 10:
                robot.stop()
                time.sleep(0.1)
                print("Heading is too far off to fix: ", current_heading)



        time.sleep(0.2)

    print("Abandon ship!")
    robot.stop()
    return False


def find_the_color(robot, sb):
    dc = DataContainer()
    btn = ev3.Button()

    btn.on_up = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_RED, sb)
    btn.on_left = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_BLACK, sb)
    btn.on_right = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_BLUE, sb)
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)


def put_down_the_beacon(robot):
    robot.arm_down()


class MyDelegate(object):

    def __init__(self):
        self.running = True


class DataContainer(object):

    def __init__(self):
        self.running = True


def drive_to_color(button_state, robot, color_to_seek, sb):
    if button_state:
        ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()

        color_sensor = ev3.ColorSensor()
        # robot.right_motor.run_forever(speed_sp=sb.getSpeed())
        # robot.left_motor.run_forever(speed_sp=sb.getSpeed())

        robot.turn_degrees(sb.getTurn(), sb.getSpeed())

        robot.drive(sb.getSpeed(), sb.getSpeed())
        while True:
            current_color = color_sensor.color
            time.sleep(0.1)
            if current_color == color_to_seek:
                robot.right_motor.stop(speed_sp = 0)
                robot.left_motor.stop(speed_sp = 0)
                ev3.Sound.speak('stop').wait()
                break
        robot.stop()
        if color_to_seek == 5:
            put_down_the_beacon(robot)


def handle_shutdown(button_state, dc):
    if button_state:
        dc.running = False



main()