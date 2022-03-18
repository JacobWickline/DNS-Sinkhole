#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:36:22 2021

@author: jacobwickline
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

class Login(QWidget):
    def __init__(self):
        super().__init__()
        
        login_status = False
        
        self.setWindowTitle("Login")
        self.setFixedSize(300, 125)
        layout = QGridLayout()
        
        label_username = QLabel('<font size="5"> Username </font>')
        self.edit_username = QLineEdit()
        label_password = QLabel('<font size="5"> Password </font>')
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.edit_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.edit_password, 1, 1)
        
        login_button = QPushButton("Login")
        cancel_button = QPushButton("Cancel")
        layout.addWidget(login_button, 2, 0)
        layout.addWidget(cancel_button, 2, 1)
        
        login_button.clicked.connect(self.login_check)
        cancel_button.clicked.connect(lambda:self.close())
        
        
        self.setLayout(layout)
        
    def login_check(self):
        msg = QMessageBox()
        
        if self.edit_username.text() == "username" and self.edit_password.text() == 'password':
            login_status = True
            self.close()
                
        else:
            msg.setWindowTitle("Incorrect Login")
            msg.setText("Incorrect Username and Password Combination")
            msg.exec_()
        
if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Login()
	form.show() 
	sys.exit(app.exec_())