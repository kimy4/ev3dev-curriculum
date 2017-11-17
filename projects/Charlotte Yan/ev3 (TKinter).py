#Charlotte Yan
#LEGO 15
#ev3 -- TKinter


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


def main():
    ev3.Sound.speak("remote drive").wait()
    print("remote drive")

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()



main()