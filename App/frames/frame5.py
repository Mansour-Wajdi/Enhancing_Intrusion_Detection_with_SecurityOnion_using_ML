from frames.base_frame import BaseFrame
import tkinter
import customtkinter
import get_pcaps_import
from threading import Thread, Event
import time

class MyFrame5(BaseFrame):

    def init_widgets(self):

        self.create_text_label("Interval:", 14)
        self.time_value_entry = self.create_entry(14, 0, placeholder_text="10")
        # Combobox for time unit (seconds, minutes, hours)
        self.time_unit_combobox = self.create_combobox(["seconds", "minutes", "hours"])
        self.time_unit_combobox.grid(row=14, column=2, padx=200, pady=10, sticky="e")
        # Button to start the function
        self.start_button = self.create_button("Start", command=self.start)
        self.start_button.grid(row=4,column=0, padx=10, pady=10, sticky="w")

        # Button to stop the function
        self.stop_button = self.create_button("Stop", command=self.stop, state=customtkinter.DISABLED)
        self.stop_button.grid(row=6,column=0, padx=10, pady=10, sticky="w")
        # Event to control the stopping of the thread
        self.stop_event = Event()

    def periodic_function(self):
        while not self.stop_event.is_set():
            print("Function executed!")
            time.sleep(2)  # Run every 2 seconds





    def start(self):
        # Disable start button and enable stop button
        self.start_button.configure(state=customtkinter.DISABLED)
        self.stop_button.configure(state=customtkinter.NORMAL)

        # Clear the stop event
        self.stop_event.clear()

        # Start the periodic function in a separate thread
        self.thread = Thread(target=self.periodic_function)
        self.thread.start()

    def stop(self):
        # Set the stop event
        self.stop_event.set()

        # Wait for the thread to stop
        self.thread.join()

        # Enable start button and disable stop button
        self.start_button.configure(state=customtkinter.NORMAL)
        self.stop_button.configure(state=customtkinter.DISABLED)
