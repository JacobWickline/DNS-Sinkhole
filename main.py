"""
Created on Nov 10 11:03:22 2021

@author: jacobwickline
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setting the title of the window
        self.setWindowTitle("The Defenders")

        #Setting the size of the window
        self.Width = 800
        self.height = 600
        self.resize(self.Width, self.height)

        #Adding buttons
        self.home_button = QPushButton("Home Screen", self)
        self.blacklist_button = QPushButton("Blacklist", self)
        self.whitelist_button = QPushButton("Whitelist", self)

        #Connecting click functionality to buttons
        self.home_button.clicked.connect(self.button1)
        self.blacklist_button.clicked.connect(self.button2)
        self.whitelist_button.clicked.connect(self.button3)

        #Adding UI tabs
        self.tab1 = self.homescreen_ui()
        self.tab2 = self.blacklist_ui()
        self.tab3 = self.whitelist_ui()

        self.init_UI()

    def init_UI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.home_button)
        left_layout.addWidget(self.blacklist_button)
        left_layout.addWidget(self.whitelist_button)

        left_layout.addStretch(5)
        left_layout.setSpacing(20)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("tab_bar")

        self.right_widget.addTab(self.tab1, "")
        self.right_widget.addTab(self.tab2, "")
        self.right_widget.addTab(self.tab3, "")

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    #UI code below
    def homescreen_ui(self):
        self.dns_sinkhole = False

        main_layout = QVBoxLayout()
        
        homescreen_title = QLabel("Welcome User!")
        homescreen_title.setFont(QFont("Arial", 40))
        homescreen_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(homescreen_title)
        main_layout.addStretch(2)
        
        self.dns_sinkhole_status = QLabel("DNS Sinkhole Status: OFFLINE")
        self.dns_sinkhole_status.setFont(QFont("Arial", 16))
        self.dns_sinkhole_status.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.dns_sinkhole_status)

        self.online_button = QPushButton("ON", self)
        main_layout.addWidget(self.online_button)
        self.online_button.clicked.connect(self.online_button_click)

        self.offline_button = QPushButton("OFF", self)
        main_layout.addWidget(self.offline_button)
        self.offline_button.clicked.connect(self.offline_button_click)

        main_layout.addStretch(5)

        main = QWidget()
        main.setLayout(main_layout)
        return main

    def blacklist_ui(self):
        main_layout = QVBoxLayout()

        blacklist_title = QLabel("Blacklist")
        blacklist_title.setFont(QFont("Arial", 40))
        blacklist_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(blacklist_title)

        main_layout.addWidget(QLabel("Enter a valid IP to blacklist"))

        self.blacklist_textbox = QLineEdit(self)
        main_layout.addWidget(self.blacklist_textbox)

        self.add_button_blacklist = QPushButton("Add", self)
        main_layout.addWidget(self.add_button_blacklist)
        self.add_button_blacklist.clicked.connect(self.blacklist_add_button_click)
        main_layout.addStretch(3)

        self.blacklist = QListWidget()
        
        #Code for reading through the config file and adding it to the list
        filepath = "/etc/dnsmasq.d/blackhole.conf"
        self.blacklist_count = 0

        with open(filepath) as file:
            for line in file:
                self.blacklist_count += 1
                self.blacklist.insertItem(self.blacklist_count, line.rstrip())

        #blacklist.insertItem(0, "Blacklisted domains go here")
        main_layout.addWidget(self.blacklist)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)

        return main

    def whitelist_ui(self):
        main_layout = QVBoxLayout()

        whitelist_title = QLabel("Whitelist")
        whitelist_title.setFont(QFont("Arial", 40))
        whitelist_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(whitelist_title)

        main_layout.addWidget(QLabel("Enter a valid IP to whitelist"))

        self.whitelist_textbox = QLineEdit(self)
        main_layout.addWidget(self.whitelist_textbox)

        self.add_button_whitelist = QPushButton("Add", self)
        main_layout.addWidget(self.add_button_whitelist)
        self.add_button_whitelist.clicked.connect(self.whitelist_add_button_click)
        main_layout.addStretch(3)
        
        self.whitelist = QListWidget()
        
        #Code for reading through the config file and adding it to the list
        filepath = "/etc/dnsmasq.d/whitelist.conf"
        self.whitelist_count = 0

        with open(filepath) as file:
            for line in file:
                self.whitelist_count += 1
                self.whitelist.insertItem(self.whitelist_count, line.rstrip())
        
        #whitelist.insertItem(0, "Whitelisted domains go here")
        main_layout.addWidget(self.whitelist)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    #Button click code below
    def online_button_click(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setWindowTitle("Alert")
        message.setText("DNS Sinkhole already running!")

        if self.dns_sinkhole == True:
            message.exec_()
        else:
            self.dns_sinkhole_status.setText("DNS Sinkhole Status: ONLINE")
            self.dns_sinkhole = True
            os.system("sudo systemctl start dnsmasq")

    def offline_button_click(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setWindowTitle("Alert")
        message.setText("DNS Sinkhole is not running!")

        if self.dns_sinkhole == False:
            message.exec_()
        else:
            self.dns_sinkhole_status.setText("DNS Sinkhole Status: OFFLINE")
            self.dns_sinkhole = False
            os.system("sudo systemctl stop dnsmasq")
            
    def blacklist_add_button_click(self):
        file = open("blackhole.conf", "a")
        text = "server=/" + self.blacklist_textbox.text() + "/"
        file.write("\n" + text)
        self.blacklist.insertItem(self.blacklist_count, text)
        self.blacklist_textbox.clear()
        file.close()
        
    def whitelist_add_button_click(self):
        file = open("whitelist.conf", "a")
        text = "server=/" + self.whitelist_textbox.text() + "/"
        file.write("\n" + text)
        self.whitelist.insertItem(self.whitelist_count, text)
        self.whitelist_textbox.clear()
        file.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())