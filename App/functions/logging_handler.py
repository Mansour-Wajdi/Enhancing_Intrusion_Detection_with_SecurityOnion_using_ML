import logging
import tkinter

class TextboxLoggerHandler(logging.Handler):
    def __init__(self, textbox_widget):
        logging.Handler.__init__(self)
        self.textbox_widget = textbox_widget

    def emit(self, record):
        msg = self.format(record)
        self.textbox_widget.configure(state='normal')  # Enable the widget
        self.textbox_widget.insert(tkinter.END, msg + '\n')  # Add the new message
        self.textbox_widget.configure(state='disabled')  # Disable the widget
        self.textbox_widget.see(tkinter.END)  # Ensure the latest log is visible
