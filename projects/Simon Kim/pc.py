import mqtt_remote_method_calls as com
import tkinter
from tkinter import  ttk


def main():
    root = tkinter.Tk()
    root.title = "User Input"
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 3)
    drive_to_color = ttk.Label(main_frame, text="drive_to_color: White, Black, Blue, red, or yellow")

    drive_to_color.grid(row=0, column=0)
    drive_to_color_entry = ttk.Entry(main_frame, width=20)
    drive_to_color_entry.grid(row=1, column=0)

    submit_button = ttk.Button(main_frame, text="Color")
    submit_button.grid(row=2, column=0)
    submit_button['command'] = lambda: button_callbacks_for_ev3(mqtt_client, drive_to_color_entry)

    root.mainloop()


def button_callbacks_for_ev3(mqtt_client, drive_to_color_entry):
    print("In callback", drive_to_color_entry.get())

    if drive_to_color_entry.get() == "White":
        print("road")
        mqtt_client.send_message("deliver_the_pizza", [drive_to_color_entry.get()])
    if drive_to_color_entry.get() == "Blue":
        print("highway")
        mqtt_client.send_message("deliver_the_pizza", [drive_to_color_entry.get()])
    if drive_to_color_entry.get() == "Red":
        print("Stop")
        mqtt_client.send_message("drive_to_color", [drive_to_color_entry.get()])
    if drive_to_color_entry.get() == "Black":
        print("stop")
        mqtt_client.send_message("deliver_the_pizza", [drive_to_color_entry.get()])
    if drive_to_color_entry.get() == "Yellow":
        print("stop")
        mqtt_client.send_message("deliver_the_pizza", [drive_to_color_entry.get()])





main()

