"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor=ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor

        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy

        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

    def drive_inches(self, inches, speed):
        self.inches = inches
        self.speed = speed

        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected


        degree_per_inch = 90
        motor_turns_needed_in_degrees = inches * degree_per_inch

        left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=speed,
                                  stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees,
                                   speed_sp=speed,stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        self.degrees_to_turn = degrees_to_turn
        self.turn_speed_sp = turn_speed_sp

        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_to_rel_pos(position_sp=-degrees_to_turn*5, speed_sp=turn_speed_sp,
                                 stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(position_sp=degrees_to_turn*5, speed_sp=turn_speed_sp,
                                   stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        touch_sensor = ev3.TouchSensor()

        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        arm_revolutions_for_full_range = 14.2 * 360
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=-900)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        arm_motor.position = 0

    def arm_up(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        touch_sensor = ev3.TouchSensor()

        arm_motor.run_to_rel_pos(position_sp=14.2 * 360, speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

    def arm_down(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        touch_sensor = ev3.TouchSensor()

        arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

        ev3.Sound.speak("Goodbye").wait()
        print('Goodbye')

    def loop_forever(self):
            # This is a convenience method that I don't really recommend for most programs other than m5.
            #   This method is only useful if the only input to the robot is coming via mqtt.
            #   MQTT messages will still call methods, but no other input or output happens.
            # This method is given here since the concept might be confusing.
        btn = ev3.Button()
        self.running = True
        while self.running and not btn.backspace:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.
        self.shutdown()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def drive(self,left_speed,right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def seek_beacon(self):
        forward_speed = 300
        turn_speed = 100
        beacon_seaker = ev3.BeaconSeeker(channel=1)

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seaker.heading
            current_distance = beacon_seaker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.drive(turn_speed, -turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    if current_distance == 0:
                        self.drive_inches(4.5, forward_speed)
                        self.stop()
                        print("Found the beacon!")
                        return True
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 1:
                        self.drive(forward_speed, forward_speed)
                        time.sleep(0.1)
                if 2 < math.fabs(current_heading) < 10:
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                        time.sleep(0.1)
                        print("Adjusting heading right: ", current_heading)

                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                        time.sleep(0.1)
                        print("Adjusting heading left: ", current_heading)

                if math.fabs(current_heading) > 10:
                    self.stop()
                    time.sleep(0.1)
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)

            print("Abandon ship!")
            self.stop()
            return False


                # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
