import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QMessageBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import threading
import time
from script import main as scraper_main

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home Page")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.initUI()
        self.noOfThread = 0
        self.stop_flag = threading.Event()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Problemset Codeforces")
        self.label.setFont(QFont("Arial", 24))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.thread_input_layout = QHBoxLayout()
        self.thread_input = QLineEdit(self)
        self.thread_input.setPlaceholderText("Enter the number of threads")
        self.thread_input.setFont(QFont("Arial", 14))
        self.thread_input.setFixedHeight(40)
        self.thread_input.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")
        self.thread_input_layout.addWidget(self.thread_input)

        self.test_button = QPushButton("ThreadUP")
        self.test_button.setFont(QFont("Arial", 16))
        self.test_button.setFixedHeight(40)
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; 
                color: white; 
                border: none; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
        """)
        self.test_button.clicked.connect(self.test_input)
        self.thread_input_layout.addWidget(self.test_button)
        
        layout.addLayout(self.thread_input_layout)

        self.table = QTableWidget(0, 4)  
        self.table.setHorizontalHeaderLabels(["Thread ID","Problem ID", "Problem Name", "Tag"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setFixedHeight(50)  
        self.table.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Scraping")
        self.start_button.setFont(QFont("Arial", 16))
        self.start_button.setFixedHeight(50)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #397d3d;
            }
        """)
        self.start_button.clicked.connect(self.start_scraping)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Scraping")
        self.stop_button.setFont(QFont("Arial", 16))
        self.stop_button.setFixedHeight(50)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white; 
                border: none; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.stop_button.clicked.connect(self.stop_scraping)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_row(self, thread_id, problem_id, problem_name, tags):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        self.table.setItem(row_position, 0, QTableWidgetItem(thread_id))
        self.table.setItem(row_position, 1, QTableWidgetItem(problem_id))
        self.table.setItem(row_position, 2, QTableWidgetItem(problem_name))
        self.table.setItem(row_position, 3, QTableWidgetItem(tags))

    def start_scraping(self):
        chromedriver_path = "./chromedriver"
        self.stop_flag.clear()
        self.scraping_thread = threading.Thread(target=scraper_main, args=(chromedriver_path, self.noOfThread, self, self.stop_flag))
        self.scraping_thread.start()

    def stop_scraping(self):
        self.stop_flag.set()
        print("Stop scraping...")

    def test_input(self):
        print(f"Entered number of threads: {self.thread_input.text()}")
        self.noOfThread = self.thread_input.text()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()

    sys.exit(app.exec_())
