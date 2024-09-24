from frames.base_frame import BaseFrame
import tkinter
import customtkinter
import logging
from functions.logging_handler import TextboxLoggerHandler
from prediction_function import predict
import pandas as pd


class MyFrame3(BaseFrame):

    def init_widgets(self):

        # Initialize predict section
        self._init_predict_section()
        self.logger5 = self._init_logging_display("Logger5", 3)
        # Initialize logging setup
        self.log_display5 = self._init_logging_display("Logger5", 3)

        # Initialize results section
        self._init_results_section()

    def _init_predict_section(self):
        """Initialize widgets for the prediction section."""
        self.create_label("____ Predict ____________________________", 0)
        label_text = "The default csv file is './csv_files/featrues_df.csv',\nif you need to select another file click 'load csv' button"
        self.create_text_label(label_text, 1)
        self.selected_file = None
        self.create_button("Load csv", lambda: self.load_csv()).grid(row=1, column=0, padx=450, pady=10, sticky="sw")
        self.create_button("Predict", lambda: self.get_prediction(self.logger5)).grid(row=2, column=0, padx=10, pady=10, sticky="e")

    def _init_logging_display(self, logger_name, row):
        """Initialize logging display and return logger instance."""
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        log_display = self.create_log_display(row, 0)
        handler = TextboxLoggerHandler(log_display)
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        return logger

    def _init_results_section(self):
        """Initialize widgets for the results section."""
        self.create_label("____ Results ___________________________", 9)
        self.create_button("Show", lambda: self.show_data()).grid(row=10, column=0, padx=10, pady=10, sticky="e")

    def show_data(self):
        """Display data in a separate window."""
        try:
            del df
        except:
            pass
        df = pd.read_csv(r'./csv_files/attacks.csv')
        self.display_dataframe_in_window(df)

    def get_selected_file(self):
        """Return the selected file."""
        return self.selected_file

    def load_csv(self):
        """Load CSV file and print selected path."""
        selected_file = self.load_file()
        if selected_file:
            print(f"Selected file: {selected_file}")
        else:
            print("No file selected.")

    def get_prediction(self, logger5):
        """Execute prediction and log results."""
        logger5.info("Predicting...")
        csv_path = './csv_files/featrues_df.csv'
        if self.selected_file:
            csv_path = self.selected_file

        predict(csv_path, logger5)
        logger5.info("Done.")
