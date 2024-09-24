from frames.base_frame import BaseFrame
import tkinter
from Elasticsearch_Data_Extraction import extract_data_from_elasticsearch
from functions.test_elasticsearch_connection import connect_elasticsearch
import pandas as pd
import logging
from functions.logging_handler import TextboxLoggerHandler
import get_pcaps_import
import get_pcaps_standalone
from extract_features import analyze_pcap_files
from prediction_function import predict
import customtkinter
from threading import Thread, Event
import time
import asyncio


class MyFrame4(BaseFrame):
    
    def init_widgets(self):
        """Initialize the UI widgets."""
        
        # Connect to Elasticsearch section
        self._setup_elasticsearch_section()
        
        # Request alerts section
        self._setup_request_alerts_section()
        
        # periodic runing section
        self.init_periodic_widgets()
        # Results section
        #self._setup_results_section()

    # ------------------- UI Sections Setup -------------------
    
    def _setup_elasticsearch_section(self):
        """Setup UI elements for Elasticsearch connection."""
        self.create_label("____ Automation Setup ______________________", 0)
        self.create_text_label("____Elasticsearch credentials________", 1)

        self.create_text_label("Server", 2)
        self.create_entry(2, 0, placeholder_text="IP address", placeholder="https://192.168.43.10:9200")
        self.create_text_label("Username", 3)
        self.create_entry(3, 0, placeholder_text="username", placeholder="jupyter")
        self.create_text_label("Password", 4)
        self.create_entry(4, 0, placeholder_text="password", show="*", placeholder="zqjdi;qnsour")
        
        self.create_text_label("____SSH Credentials________", 5)
        self.create_text_label("Remote Host", 6)
        self.create_entry(6, 0, placeholder_text="IP address", placeholder="192.168.43.10")
        self.create_text_label("Remote Username", 7)
        self.create_entry(7, 0, placeholder_text="username", placeholder="wajdi")
        self.create_text_label("Remote Password", 8)
        self.create_entry(8, 0, placeholder_text="password", show="*", placeholder="0000")


        # Logging setup for Elasticsearch
        self.log_display1 = self.create_log_display(20, 0,height=400)
        self.logger1 = self._setup_logger("Logger1", self.log_display1)
        
        #self.create_button("test", lambda: self.automation()).grid(row=15, column=0, padx=10, pady=10, sticky="e")
        
        self.create_button("Show Results", lambda: self.show_data()).grid(row=17, column=0, padx=10, pady=10, sticky="e")

    def _setup_request_alerts_section(self):
        """Setup UI elements for requesting alerts."""
        #self.create_label("____ request alerts ___________________________", 10)
        self.create_text_label("____Security Onion node type________", 11)
        options = ["standalone", "import"]
        selected_option = tkinter.StringVar()
        radiobuttons = self.create_radiobuttons(options, 12, 0, variable=selected_option, orientation="horizontal")
        self.create_text_label("____Alerts Severity________", 13)
        self.create_checkboxes(["low", "medium", "high"], 14, 0, orientation="horizontal")


    def _setup_logger(self, logger_name, log_display):
        """Helper method to set up logger."""
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        handler = TextboxLoggerHandler(log_display)
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        return logger

    # ------------------- Main Functions -------------------
    
    def automation(self):
        self.retrive_alerts()
        self.get_pcap(self.logger1)
        self.extract()
        self.get_prediction(self.logger1)

    def get_pcap(self, logger4):
        remote_host = self.get_remote_host()
        remote_username = self.get_remote_username()
        remote_password = self.get_remote_password()
        version = self.get_option()
        csv_path='./csv_files/flow_info.csv'

        if version == 'import':
            get_pcaps_import.process_pcap_requests(remote_host, remote_username, remote_password,csv_path, logger4)
        elif version == 'standalone':
            get_pcaps_standalone.process_pcap_requests(remote_host, remote_username, remote_password,csv_path, logger4)
        else:
            logger4.error("no version is selected, please select a version")

    def extract(self):
        dir_path='./pcap_files'
        csv_path='./csv_files/flow_info.csv'
        print(dir_path,csv_path)
        analyze_pcap_files(dir_path,csv_path)

    def get_prediction(self, logger5):
        """Execute prediction and log results."""
        logger5.info("Predicting...")
        csv_path = './csv_files/featrues_df.csv'
        predict(csv_path, logger5)
        logger5.info("Done.")


    def Connect_to_elastic(self):
        """Connect to Elasticsearch."""
        elastic_host = self.get_ip_address()
        username = self.get_username()
        password = self.get_password()
        connect_elasticsearch(elastic_host, username, password,self.logger1)

    def retrive_alerts(self):
        """Retrieve alerts from Elasticsearch."""
        elastic_host = self.get_ip_address()
        username = self.get_username()
        password = self.get_password()
        version = self.get_version()
        severity = self.get_severity()
        extract_data_from_elasticsearch(elastic_host, username, password, version, severity,self.logger1)

    def show_data(self):
        """Display data in a new window."""
        try:
            del df
        except:
            pass
        df = pd.read_csv('./csv_files/attacks.csv')
        self.display_dataframe_in_window(df)


    # ------------------- Periodic Function setup -------------------
    def init_periodic_widgets(self):
        # Button to start the function
        self.start_button = self.create_button("Start", command=self.start)
        self.start_button.grid(row=15,column=0, padx=10, pady=10, sticky="e")

        # Combobox for time unit (seconds, minutes, hours)
        self.create_text_label("Interval:", 15)
        self.create_entry(15, 0, placeholder_text="10", placeholder="10")
        self.time_unit_combobox = self.create_combobox(["seconds", "minutes", "hours"])
        self.time_unit_combobox.grid(row=16,column=0, padx=250)


        # Button to stop the function
        self.stop_button = self.create_button("Stop", command=self.stop, state=customtkinter.DISABLED)
        self.stop_button.grid(row=16,column=0, padx=10, pady=10, sticky="e")
        # Event to control the stopping of the thread
        self.stop_event = Event()


    def periodic_function(self):
        # Setup a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        unit = self.time_unit_combobox.get()
        delay_value=int(self.get_all_widget_data()['entry_7'])
        if unit == "minutes":
            delay_time = delay_value * 60
        elif unit == "hours":
            delay_time = delay_value * 3600
        else:  # default to seconds
            delay_time = delay_value

        try:
            while not self.stop_event.is_set():
                self.automation()
                print("Function executed!")
                print(delay_time)
                time.sleep(delay_time) 
        finally:
            loop.close()

    """
    def periodic_function(self):
        while not self.stop_event.is_set():
            self.automation()
            print("Function executed!")
            time.sleep(10)  # Run every 2 seconds
    """
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


    # ------------------- Getters -------------------
    
    def get_all_widget_data(self):
        """Retrieve data from all widgets."""
        return super().get_all_widget_data()

    def get_ip_address(self):
        """Get IP address."""
        return self.get_all_widget_data().get('entry_1', None)

    def get_username(self):
        """Get username."""
        return self.get_all_widget_data().get('entry_2', None)

    def get_password(self):
        """Get password."""
        return self.get_all_widget_data().get('entry_3', None)

    def get_remote_host(self):
        data = self.get_all_widget_data()
        return data.get('entry_4', None)

    def get_remote_username(self):
        data = self.get_all_widget_data()
        return data.get('entry_5', None)

    def get_remote_password(self):
        data = self.get_all_widget_data()
        return data.get('entry_6', None)

    def get_option(self):
        data = self.get_all_widget_data()
        return data.get('radiobutton_1', None)

    def get_version(self):
        """Get version."""
        return self.get_all_widget_data().get('radiobutton_1', None)

    def get_severity(self):
        """Get severity level."""
        severity_data = self.get_all_widget_data().get('checkboxgroup_1', {})
        severity = []
        for key, value in severity_data.items():
            if value:
                if key == 'low':
                    severity.append('3')
                elif key == 'medium':
                    severity.append('2')
                elif key == 'high':
                    severity.append('1')
        return severity



