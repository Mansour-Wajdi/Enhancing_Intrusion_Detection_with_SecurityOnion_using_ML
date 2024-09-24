from frames.base_frame import BaseFrame
import tkinter
from Elasticsearch_Data_Extraction import extract_data_from_elasticsearch
from functions.test_elasticsearch_connection import connect_elasticsearch
import pandas as pd
import logging
from functions.logging_handler import TextboxLoggerHandler

class Home(BaseFrame):
    
    def init_widgets(self):
        """Initialize the UI widgets."""
        
        # Connect to Elasticsearch section
        self._setup_elasticsearch_section()
        
    # ------------------- UI Sections Setup -------------------
    
    def _setup_elasticsearch_section(self):
        """Setup UI elements for Elasticsearch connection."""
        self.create_label("____ Hi ____________________________", 0)
        self.create_text_label("Username", 2)
