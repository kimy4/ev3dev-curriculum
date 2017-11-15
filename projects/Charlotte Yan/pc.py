
#Charlotte Yan
#LEGO 15
#pc control


import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):

    def print_message(self, message):
        print("Message received:", message)


def main():
    root = tkinter.Tk()
    root.title("Speed and degrees")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    left_side_label = ttk.Label(main_frame, text="Left")
    left_side_label.grid(row=2, column=0)

    left_degree_entry = ttk.Entry(main_frame, width=8)
    left_degree_entry.grid(row=5, column=0)

    left_degree_label = ttk.Label(main_frame, text='(degree=0-180)')
    left_degree_label.grid(row=6, column=0)

    right_side_label = ttk.Label(main_frame, text="Right")
    right_side_label.grid(row=2, column=2)

    right_degree_entry = ttk.Entry(main_frame, width=8)
    right_degree_entry.grid(row=5, column=2)

    right_degree_label = ttk.Label(main_frame, text='(degree=0-180)')
    right_degree_label.grid(row=6, column=2)

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

    turn_button = ttk.Button(main_frame, text='Turn')
    turn_button.grid(row=5, column=1)
    turn_button['command'] = lambda: turn_degrees(mqtt_client, left_degree_entry.get(), right_degree_entry.get())
    # root.bind('<Turn>', lambda event:turn_degrees(mqtt_client, left_degree_entry.get(), right_degree_entry.get()))

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def send_command(mqtt_client, color):
    print('Send color = {}', format(color))
    mqtt_client.send_message('Find the color', [color])


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


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

main()