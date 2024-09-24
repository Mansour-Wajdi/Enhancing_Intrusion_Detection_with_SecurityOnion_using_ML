import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

def display_dataframe_in_window(dataframe):
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

    sys.exit(app.exec_())

# Example usage:
data = {'Column1': range(1, 101),
        'Column2': range(101, 201)}
df = pd.DataFrame(data)

display_dataframe_in_window(df)
