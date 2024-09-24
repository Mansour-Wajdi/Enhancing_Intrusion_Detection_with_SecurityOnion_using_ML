from frames.base_frame import BaseFrame
import tkinter
import customtkinter
import pandas as pd
import get_pcaps_import
import get_pcaps_standalone
from extract_features import analyze_pcap_files
from functions.test_ssh_connection import test_ssh_connection
import logging
from functions.logging_handler import TextboxLoggerHandler


class MyFrame2(BaseFrame):

    def init_widgets(self):

        # Section to connect to Elasticsearch
        self._init_connect_section()

        # Section to load csv
        self._init_csv_load_section()

        # Section to get pcap
        self._init_get_pcap_section()

        # Section to extract features
        self._init_extract_features_section()

        # Section to show results
        self._init_show_results_section()

    def _init_connect_section(self):
        self.create_label("____ Connect ____________________________", 0)
        self.create_text_label("Remote Host", 1)
        self.create_entry(1, 0, placeholder_text="IP address", placeholder="192.168.43.10")
        self.create_text_label("Remote Username", 2)
        self.create_entry(2, 0, placeholder_text="username", placeholder="wajdi")
        self.create_text_label("Remote Password", 3)
        self.create_entry(3, 0, placeholder_text="password", show="*", placeholder="0000")

        self.log_display3 = self._init_logging_display("Logger3", 5)
        self.create_button("Connect", lambda: self.test_connection(self.logger3)).grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.log_display3 = self._init_logging_display("Logger3", 5)
        self.create_button("Connect", lambda: self.test_connection(self.logger3)).grid(row=4, column=0, padx=10, pady=10, sticky="e")

    def _init_csv_load_section(self):
        self.create_label("____ PCAP Fetching ____________________________", 6)
        label_text = "The default csv file is './csv_files/flow_info.csv',\nif you need to select another file click 'load csv' button"
        self.create_text_label(label_text, 7)
        self.selected_file = None
        self.create_button("Load csv", lambda: self.load_file()).grid(row=7, column=0, padx=450, pady=10, sticky="sw")

    def _init_get_pcap_section(self):
        self.create_text_label("Security Onion node type", 9)
        options = ["standalone", "import"]
        selected_option = tkinter.StringVar()
        radiobuttons = self.create_radiobuttons(options, 10, 0, variable=selected_option, orientation="horizontal")

        self.log_display4 = self._init_logging_display("Logger4", 15)
        self.create_button("Get PCAPs", lambda: self.get_pcap(self.logger4)).grid(row=14, column=0, padx=10, pady=10, sticky="e")

    def _init_extract_features_section(self):
        self.create_label("____ Extract Features ___________________________", 17)
        label_text = "the default directory of pcap files is './pcap_files',\nif you need to select another directory click 'change pcap dir' button"
        self.create_text_label(label_text, 18)
        self.selected_dir = None
        self.create_button("Change pcap dir", lambda: self.load_dir()).grid(row=18, column=0, padx=450, pady=10, sticky="sw")
        self.create_button("Extract Features", lambda: self.extract()).grid(row=19, column=0, padx=10, pady=10, sticky="e")

    def _init_show_results_section(self):
        self.create_label("____ Results ___________________________", 20)
        self.create_button("Show", lambda: self.show_data()).grid(row=21, column=0, padx=10, pady=10, sticky="e")

    def _init_logging_display(self, logger_name, row):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        log_display = self.create_log_display(row, 0)
        handler = TextboxLoggerHandler(log_display)
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        
        # Set logger to instance variable
        if logger_name == "Logger3":
            self.logger3 = logger
        elif logger_name == "Logger4":
            self.logger4 = logger
            
        return log_display


    # ------------------- Main Functions -------------------

    def add_message_to_first_display(self, message):
        self.append_to_log_display(self.log_display3, message)

    def add_message_to_second_display(self, message):
        self.append_to_log_display(self.log_display4, message)

    def get_pcap(self, logger4):
        remote_host = self.get_remote_host()
        remote_username = self.get_remote_username()
        remote_password = self.get_password()
        version = self.get_option()
        csv_path='./csv_files/flow_info.csv'
        if self.selected_file:
            csv_path=self.selected_file

        if version == 'import':
            get_pcaps_import.process_pcap_requests(remote_host, remote_username, remote_password,csv_path, logger4)
        elif version == 'standalone':
            get_pcaps_standalone.process_pcap_requests(remote_host, remote_username, remote_password,csv_path, logger4)
        else:
            logger4.error("no version is selected, please select a version")


    def test_connection(self,logger3):
        remote_host = self.get_remote_host()
        remote_username = self.get_remote_username()
        remote_password = self.get_password()
        test_ssh_connection(remote_host, remote_username, remote_password, logger3)
         
    def show_data(self):
        try:
            del df
        except: 
            pass
        df=pd.read_csv(r'./csv_files/featrues_df.csv')
        self.display_dataframe_in_window(df)

    def extract(self):
        dir_path='./pcap_files'
        if self.selected_dir:
            dir_path=self.selected_dir
        csv_path='./csv_files/flow_info.csv'
        if self.selected_file:
            csv_path=self.selected_file
        print(dir_path,csv_path)
        analyze_pcap_files(dir_path,csv_path)

    
    # ------------------- Getters -------------------
    def get_remote_host(self):
        data = self.get_all_widget_data()
        return data.get('entry_1', None)

    def get_remote_username(self):
        data = self.get_all_widget_data()
        return data.get('entry_2', None)

    def get_password(self):
        data = self.get_all_widget_data()
        return data.get('entry_3', None)

    def get_option(self):
        data = self.get_all_widget_data()
        return data.get('radiobutton_1', None)

    def get_selected_file(self):
        return self.selected_file

    def get_selected_dir(self):
        return self.selected_dir
