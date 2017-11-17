import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
import traceback

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

black_color_number = 1
blue_color_number = 2
yellow_color_number = 4
red_color_number = 5
white_color_number = 6

print('--------------------------------')
print('CSSE120 Final Project: Simon Kim')
print('--------------------------------')


class MyDelegate(object):
    def __init__(self, robot):
        self.running = True
        self.robot = robot

    def deliver_the_pizza(self, deliver_the_pizza):

        self.robot.left_motor.run_forever(speed_sp=200)
        self.robot.right_motor.run_forever(speed_sp=200)

        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + deliver_the_pizza).wait()
        self.robot.turn_degrees(90, 300)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        self.robot.drive_inches(22, 300)
        self.robot.arm_up()
        time.sleep(5.0)

        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + deliver_the_pizza).wait()
        ev3.Sound.speak("You have successfully delivered the" + deliver_the_pizza + "pizza")


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    btn = ev3.Button()

    btn.on_up = lambda state: deliver_the_pizza(state, robot, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: deliver_the_pizza(state, robot, ev3.ColorSensor.COLOR_WHITE)
    btn.on_left = lambda state: deliver_the_pizza(state, robot, ev3.ColorSensor.COLOR_BLUE)
    btn.on_right = lambda state: deliver_the_pizza(state, robot, ev3.ColorSensor.COLOR_BLACK)

    while mqtt_client.running:
        btn.process()
        time.sleep(0.01)


def deliver_the_pizza(button_state, robot, deliver_the_pizza):

    if button_state:
        robot.left_motor.run_forever(speed_sp=200)
        robot.right_motor.run_forever(speed_sp=200)

        try:
            while True:
                found_beacon = robot.seek_beacon()
                if found_beacon:
                    ev3.Sound.speak("I got the pizza")
                    robot.arm_up()

                while robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                    time.sleep(5.0)
                robot.left_motor.stop()
                robot.right_motor.stop()
                robot.drive_inches(22, 300)
                robot.left_motor.run_forever(speed_sp=200)
                robot.right_motor.run_forever(speed_sp=200)

                while robot.color_sensor.color != deliver_the_pizza:
                    time.sleep(5.0)
                robot.left_motor.stop()
                robot.right_motor.stop()
                robot.turn_degrees(90, 150)
                robot.left_motor.stop()
                robot.right_motor.stop()
                robot.drive_inches(22, 150)
                robot.left_motor.run_forever(speed_sp=300)
                robot.right_motor.run_forever(speed_sp=300)

                while robot.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                    time.sleep(0.01)
                robot.left_motor.stop()
                robot.right_motor.stop()
                time.sleep(1)
                robot.arm_down()

            while True:

                command = input("Hit enter to seek the beacon again or enter q to quit: ")
                if command == "q":
                    break

        except:
            traceback.print_exc()
            ev3.Sound.speak("Error")

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()


main()