#Charlotte Yan
#LEGO 15
#pc control -- TKinter



import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    left_side_label = ttk.Label(main_frame, text="Left")
    left_side_label.grid(row=2, column=0)

    right_side_label = ttk.Label(main_frame, text="Right")
    right_side_label.grid(row=2, column=2)

    label2 = ttk.Label(main_frame, text='(speed=0-600)')
    label2.grid(row=4, column=0)

    label4 = ttk.Label(main_frame, text='(speed=0-600)')
    label4.grid(row=4, column=2)

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=2, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=3, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=2, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=3, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=3, column=1)
    forward_button['command'] = lambda: go_forward(mqtt_client, left_speed_entry.get(), right_speed_entry.get())
    root.bind('<Up>', lambda event: go_forward(mqtt_client, left_speed_entry.get(), right_speed_entry.get()))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=6, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=2)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=6, column=1)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))


    root.mainloop()


def send_message(mqtt_client, msg_entry):
    msg = msg_entry.get()
    msg_entry.delete(0, 'end')
    mqtt_client.send_message("print_message", [msg])


def go_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("go_forward")
    mqtt_client.send_message("drive", [int(left_speed_entry), int(right_speed_entry)])


def turn_degrees(mqtt_client, left_degree_entry, right_degree_entry):
    print('turn_degrees')
    mqtt_client.send_message('turn', [int(left_degree_entry), int(right_degree_entry)])


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


main()


