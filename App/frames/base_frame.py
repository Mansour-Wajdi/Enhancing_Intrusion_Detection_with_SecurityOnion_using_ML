import tkinter
import customtkinter
from tkinter import filedialog


import sys
import pandas as pd
from PyQt5.QtCore import Qt


class BaseFrame(customtkinter.CTkScrollableFrame):
    
    DEFAULT_FONT = ("Helvetica", 32, "bold")
    DEFAULT_BUTTON_FONT = ("Helvetica", 16, "bold")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entries = []  # Store references to Entry widgets
        self.radiobutton_vars = []  # Store references to the variables associated with Radiobuttons
        self.checkbox_vars = []  # Store references to the variables associated with Checkbuttons
        self.init_widgets()
    
    def init_widgets(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def create_label(self, text, row):
        label = customtkinter.CTkLabel(
            self, text=text, width=120, height=25, corner_radius=8,
            font=self.DEFAULT_FONT
        )
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

        return label
    
    def create_text_label(self, text, row, column=0,padx=20, pady=10, sticky="w"):
        label = customtkinter.CTkLabel(
            self, text=text, width=60, height=25, corner_radius=8,justify="left", anchor="nw",
            font=self.DEFAULT_BUTTON_FONT
        )
        label.grid(row=row, column=column, padx=padx, pady=pady , sticky=sticky)
        return label


    def create_output_label(self, results_text):
        text_var = tkinter.StringVar(value=results_text)
        label = customtkinter.CTkLabel(
            self, textvariable=text_var, fg_color=("white", "gray20"), corner_radius=8,
            font=self.DEFAULT_BUTTON_FONT, justify="left", anchor="nw"
        )
        return label, text_var

    def create_button(self, text, command,state=None):
        button = customtkinter.CTkButton(
            self, text=text, font=self.DEFAULT_BUTTON_FONT, command=command
        )

        try:
            button.configure(state=state)
        except:
            pass

        return button


    def create_entry(self, row, column, placeholder=None, **kwargs):
        entry = customtkinter.CTkEntry(self, **kwargs)
        entry.grid(row=row, column=column)
        if placeholder:
            entry.insert(0, placeholder)
        self.entries.append(entry)
        return entry

    def create_combobox(self, options):
        combobox=customtkinter.CTkComboBox(self, values=options)
        combobox.set(options[0])
        return combobox
        
    def create_radiobuttons(self, options, row, column, variable=None, orientation="vertical", **kwargs):
        """
        Creates a group of radiobuttons.
        
        Parameters:
            options (list): List of options to create radiobuttons for.
            row (int): Starting row for the radiobuttons.
            column (int): Column in which the radiobuttons should be placed.
            variable (tkinter.Variable, optional): Variable to track the selected option. Defaults to None.
            orientation (str, optional): "vertical" or "horizontal" orientation for the radiobuttons. Defaults to "vertical".
            **kwargs: Additional arguments passed to the radiobuttons.
            
        Returns:
            list: List of created radiobutton widgets.
        """
        
        if not variable:
            variable = tkinter.StringVar()
        
        radiobuttons = []
        for i, option in enumerate(options):
            rb = customtkinter.CTkRadioButton(self, text=option , variable=variable, value=option, font=self.DEFAULT_BUTTON_FONT , **kwargs)
            if orientation == "vertical":
                rb.grid(row=row + i , column=column, sticky="w")
            else:
                rb.grid(row=row, column=column, sticky="w", padx=150 * i)
            radiobuttons.append(rb)

        self.radiobutton_vars.append(variable)  # Store the variable for radiobutton value
        return radiobuttons


    def create_checkboxes(self, options, row, column, orientation="vertical", **kwargs):
        """
        Creates a group of checkboxes.
        
        Parameters:
            options (list): List of options to create checkboxes for.
            row (int): Starting row for the checkboxes.
            column (int): Column in which the checkboxes should be placed.
            orientation (str, optional): "vertical" or "horizontal" orientation for the checkboxes. Defaults to "vertical".
            **kwargs: Additional arguments passed to the checkboxes.
            
        Returns:
            dict: Dictionary containing options as keys and their respective tkinter.IntVar() as values.
        """
        
        checkbox_vars = {}
        checkboxes = {}
        for i, option in enumerate(options):
            var = tkinter.IntVar()
            checkbox_vars[option] = var
            cb = customtkinter.CTkCheckBox(self, text=option,font=self.DEFAULT_BUTTON_FONT, variable=var, **kwargs)
            if orientation == "vertical":
                cb.grid(row=row + i, column=column, sticky="w")
            else:
                cb.grid(row=row, column=column, sticky="w", padx=150 * i)
            checkboxes[option] = cb

        self.checkbox_vars.append(checkbox_vars)  # Store the dictionary of checkbox variables
        return checkbox_vars


    def create_dropdown(self, options, row, column, default=None, **kwargs):
        """
        Creates a drop-down menu (OptionMenu).
        
        Parameters:
            options (list): List of options for the dropdown.
            row (int): Row in which the dropdown should be placed.
            column (int): Column in which the dropdown should be placed.
            default (str, optional): Default value to be shown in the dropdown. If not provided, the first item from options will be taken.
            **kwargs: Additional arguments passed to the OptionMenu.
            
        Returns:
            tkinter.StringVar, tkinter.OptionMenu: Variable holding the current value of the dropdown, and the OptionMenu widget itself.
        """
        
        variable = tkinter.StringVar()
        if default:
            variable.set(default)
        else:
            variable.set(options[0])

        dropdown = customtkinter.CTkOptionMenu(self, variable, *options, **kwargs)
        dropdown.grid(row=row, column=column, sticky="w")
        
        return variable, dropdown


    def get_all_widget_data(self):
        data = {}

        # Entry data
        for i, entry in enumerate(self.entries):
            data[f"entry_{i+1}"] = entry.get()

        # Radiobutton data
        for i, var in enumerate(self.radiobutton_vars):
            data[f"radiobutton_{i+1}"] = var.get()

        # Checkbutton data
        for i, checkbox_group in enumerate(self.checkbox_vars):
            group_data = {}
            for option, var in checkbox_group.items():
                group_data[option] = bool(var.get())  # Convert int to bool for clarity
            data[f"checkboxgroup_{i+1}"] = group_data
        #print(data)
        return data



    def create_log_display(self, row, column, initial_text="",height=100):
        log_display = customtkinter.CTkTextbox(self, state='normal', width=1000, height=height)
        log_display.insert(tkinter.END, initial_text)
        log_display.configure(state='disabled')
        log_display.grid(row=row, column=column, padx=10, pady=10, sticky="w")
        return log_display

    def append_to_log_display(self, log_display, message, mode="append"):
        log_display.configure(state='normal')  # Enable the widget
        if mode == "write":
            log_display.delete(1.0, tkinter.END)  # Clear the existing content
        log_display.insert(tkinter.END, message + '\n')  # Add the new message
        log_display.configure(state='disabled')  # Disable the widget



    def load_file(self):
        """Open a window to let the user load a file and return the selected file's path."""
        file_path = filedialog.askopenfilename()
        return file_path

    def load_dir(self):
        """Open a window to let the user load a directory and return the selected file's path."""
        dir_path = filedialog.askdirectory()
        return dir_path

    def display_dataframe_in_window(self, dataframe):
        """Display a dataframe in a window using PyQt5."""
        
        import sys
        from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

        # Set the auto scaling for high DPI displays
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

        app = QApplication(sys.argv)

        main_window = QMainWindow()
        main_window.setWindowTitle('DataFrame Table')

        table_widget = QTableWidget()
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))
        table_widget.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                item = QTableWidgetItem(str(dataframe.iloc[row, col]))
                table_widget.setItem(row, col, item)

        main_window.setCentralWidget(table_widget)

        main_window.show()

        app.exec_()


