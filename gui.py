import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QMessageBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By

def login(driver, user_name, pass_word):
    codeforces_url = "https://codeforces.com/"
    driver.get(codeforces_url)

    enter_btn = driver.find_element(By.CSS_SELECTOR, 'a[href="/enter?back=%2F"]')
    enter_btn.click()

    handle_or_email = driver.find_element(By.ID, "handleOrEmail")
    handle_or_email.clear()
    handle_or_email.send_keys(user_name)

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys(pass_word)

    login_btn = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    login_btn.click()

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 500, 400)  # Set initial size
        self.setStyleSheet("background-color: #f0f0f0;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Please log in")
        self.label.setFont(QFont("Arial", 20))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setFont(QFont("Arial", 14))
        self.username.setAlignment(Qt.AlignCenter)  # Center align text
        self.username.setFixedHeight(40)
        self.username.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setFont(QFont("Arial", 14))
        self.password.setAlignment(Qt.AlignCenter)  # Center align text
        self.password.setFixedHeight(40)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.password)

        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 16))
        self.login_button.setFixedHeight(50)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        if self.username.text() == "admin" and self.password.text() == "password":
            self.accept_login()
        else:
            QMessageBox.warning(self, "Error", "Incorrect Username or Password")

    def accept_login(self):
        self.hide()
        self.home_page = HomePage()
        self.home_page.show()

    def highlight_border(self):
        sender = self.sender()  # Get the sender widget
        if sender.text():
            sender.setStyleSheet("border: 2px solid #4CAF50; border-radius: 10px; padding: 10px;")
        else:
            sender.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home Page")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.initUI()

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

        self.table = QTableWidget(0, 2)  # Initially 0 rows, 2 columns
        self.table.setHorizontalHeaderLabels(["Problem ID", "Tag"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setFixedHeight(50)  # Set header height
        self.table.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.table)

        # Adding the buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
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

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFont(QFont("Arial", 16))
        self.stop_button.setFixedHeight(50)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336; 
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

    def add_row(self, problem_id, tag):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(problem_id))
        self.table.setItem(row_position, 1, QTableWidgetItem(tag))

    def start_scraping(self):
        print("Start scraping...")

    def stop_scraping(self):
        print("Stop scraping...")

    def test_input(self):
        print(f"Entered number of threads: {self.thread_input.text()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
