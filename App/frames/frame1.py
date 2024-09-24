from frames.base_frame import BaseFrame
import tkinter
from Elasticsearch_Data_Extraction import extract_data_from_elasticsearch
from functions.test_elasticsearch_connection import connect_elasticsearch
import pandas as pd
import logging
from functions.logging_handler import TextboxLoggerHandler

class MyFrame1(BaseFrame):
    
    def init_widgets(self):
        """Initialize the UI widgets."""
        
        # Connect to Elasticsearch section
        self._setup_elasticsearch_section()
        
        # Request alerts section
        self._setup_request_alerts_section()
        
        # Results section
        self._setup_results_section()

    # ------------------- UI Sections Setup -------------------
    
    def _setup_elasticsearch_section(self):
        """Setup UI elements for Elasticsearch connection."""
        self.create_label("____ Connect ____________________________", 0)
        self.create_text_label("Server", 1)
        self.create_entry(1, 0, placeholder_text="IP address", placeholder="https://192.168.43.10:9200")
        self.create_text_label("Username", 2)
        self.create_entry(2, 0, placeholder_text="username", placeholder="jupyter")
        self.create_text_label("Password", 3)
        self.create_entry(3, 0, placeholder_text="password", show="*", placeholder="zqjdi;qnsour")
        
        # Logging setup for Elasticsearch
        self.log_display1 = self.create_log_display(5, 0)
        self.logger1 = self._setup_logger("Logger1", self.log_display1)
        
        self.create_button("Connect", lambda: self.Connect_to_elastic()).grid(row=4, column=0, padx=10, pady=10, sticky="e")

    def _setup_request_alerts_section(self):
        """Setup UI elements for requesting alerts."""
        self.create_label("____ Request Alerts ___________________________", 7)
        self.create_text_label("Security Onion node type", 8)
        options = ["standalone", "import"]
        selected_option = tkinter.StringVar()
        radiobuttons = self.create_radiobuttons(options, 9, 0, variable=selected_option, orientation="horizontal")
        self.create_text_label("Alerts Severity", 10)
        self.create_checkboxes(["low", "medium", "high"], 11, 0, orientation="horizontal")
        
        # Logging setup for request alerts
        self.log_display2 = self.create_log_display(14, 0, "")
        self.logger2 = self._setup_logger("Logger2", self.log_display2)
        
        self.create_button("Retrive Alerts", lambda: self.retrive_alerts()).grid(row=13, column=0, padx=10, pady=10, sticky="e")

    def _setup_results_section(self):
        """Setup UI elements for displaying results."""
        self.create_label("____ Results ___________________________", 15)
        self.create_button("Show", lambda: self.show_data()).grid(row=16, column=0, padx=10, pady=10, sticky="e")

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
        extract_data_from_elasticsearch(elastic_host, username, password, version, severity,self.logger2)

    def show_data(self):
        """Display data in a new window."""
        try:
            del df
        except:
            pass
        df = pd.read_csv('./csv_files/flow_info.csv')
        self.display_dataframe_in_window(df)

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

