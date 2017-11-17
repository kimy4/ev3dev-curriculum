import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import robot_controller as robo


def main():
    root = tkinter.Tk()
    root.title = "Delivery"

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    instructions = "Deliver the pizza"
    label = ttk.Label(main_frame, text=instructions)
    label.grid(columnspan=2)

    mqtt_client=com.MqttClient(robo.Snatch3r)
    mqtt_client.connect_to_ev3()

    drive_to_color = ttk.Label(main_frame, text="drive_to_color: White, Black, Blue, red, or yellow")

    # Entry
    drive_to_color.grid(row=0, column=0)
    drive_to_color_ttk = ttk.Entry(main_frame, width=20)
    drive_to_color_ttk.grid(row=1, column=0)

    submit_button = ttk.Button(main_frame, text="Color")
    submit_button.grid(row=2, column=0)
    submit_button['command'] = lambda: controller(mqtt_client, drive_to_color_ttk)

    root.mainloop()


def controller(mqtt_client, drive_to_color_entry):
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

