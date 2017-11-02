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

  Commands for the Snatch3r robot that might be useful in many different programs.
"""

import ev3dev.ev3 as ev3
import time


class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert self.left_motor.connected
        assert self.right_motor.connected
        self.arm_motor = ev3.LargeMotor(ev3.OUTPUT_A)

        assert self.arm_motor.connected

        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor.connected

    def drive_inches(self, inches, speed):
        """ Moves the robot forward the requested number of inches at a speed in degrees / second."""
        degrees_per_inch = 90
        degrees = inches * degrees_per_inch

        self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
    def drive(self, left_sp, right_sp):
        self.left_motor.run_forever(speed_sp=left_sp )
        self.right_motor.run_forever(speed_sp=right_sp)

    def turn_degree(self, degree, speed):
        """Moves the robot to a given degree at a given speed."""
        self.left_motor.run_to_rel_pos(position_sp=degree*5, speed_sp=speed)
        self.right_motor.run_to_rel_pos(position_sp=-degree*5, speed_sp=speed)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()

    def arm_calibration(self):
        """Moves the arm up and then back down to recalibrate it."""
        touch_sensor = ev3.TouchSensor()
        self.arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

        self.arm_motor.run_to_rel_pos(position_sp=-5112, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        """Moves arm up to the MAX position."""
        touch_sensor = ev3.TouchSensor()
        self.arm_motor.run_to_abs_pos(position_sp=14.2 * 360, speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Moves the arms down back to the MIN position."""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=-900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def shutdown(self):
        """Shutdown the program"""
        btn = ev3.Button()
        while btn.backspace:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Sound.speak('goodbye').wait()
            print('Goodbye')

    def loop_forever(self):
        # This is a convenience method that is only useful if the only input to the robot is coming via mqtt.
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.shutdown()
