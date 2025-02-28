"""
Filename: batch_renamer_gui_starter.py
Title: Batch File Renamer
Author: Macy Chantharak
Date Created: 2025-02-27
Date Edited: 2025-02-28
Description:
    This program launches a GUI for a batch file renamer that can
    rename files or create a copy of the file with a new file name.
Python Version: 3.13
"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# You'll need to make this ui in QtDesigner
# And convert it to a .py file using the MakeUIPy.bat file
from batch_renamer_ui import Ui_MainWindow 
# Recommend you rename this
import batch_renamer_lib as Renamer

class BatchRenamerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # UI Setup
        super().__init__()
        super(Ui_MainWindow).__init__()
        self.setupUi(self)
        # Connect button to function
        self.button_filepath_browse.clicked.connect(self.get_filepath)
        # Connect your new "Run" button to self.run_renamer
        self.button_run.clicked.connect(self.run_renamer)

        # Instance the "back end"
        self.batch_renamer = Renamer.BatchRenamer()
        
        # Show UI normal vs maximized
        self.showNormal()


    def get_filepath(self):
        """
        Open a file dialog for browsing to a folder
        """
        self.filepath = QFileDialog().getExistingDirectory()
        self.set_filepath()


    def set_filepath(self):
        """
        Set lineEdit text for filepath
        """
        self.lineedit_filepath.setText(self.filepath)
        self.update_list()

    def set_parameters(self):
        """
        Sets parameters for extension, prefix, suffix, string_to_find,
        string_to_replace, and copy from the UI.
        """
        self.extension = self.lineedit_extension.text()
        self.prefix = self.lineedit_prefix.text()
        self.suffix = self.lineedit_suffix.text()
        self.string_to_find = self.lineedit_string_to_find.text()
        self.string_to_replace = self.lineedit_string_to_replace.text()
        self.copy = self.button_copy.isChecked()
        if '/' in self.string_to_find:
            self.string_to_find = self.string_to_find.split('/')

    def update_list(self):
        """
        Clear listWidget
        Read files in filepath with os.walk
        Add files as new items
        """
        self.listWidget.clear()
        for root, dirs, files in os.walk(self.filepath):
            self.listWidget.addItems(files)

    def complete_popup(self):
        message = QMessageBox()
        message.setWindowTitle("Complete")
        message.setText('Program has completed running.\n'
                        'Check the log for information.')
        x = message.exec()
    
    def err_popup(self):
        message = QMessageBox()
        message.setWindowTitle("ERROR")
        message.setText('An error has occured!\n'
                        'Check the log for information')
        message.setIcon(QMessageBox.Icon.Critical)
        x = message.exec()


    def run_renamer(self):
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        Updates listWidget.
        """
        self.set_parameters()
        try:
            self.batch_renamer.rename_files_in_folder(self.filepath, 
                                                      self.extension, 
                                                      self.string_to_find,
                                                      self.string_to_replace,
                                                      self.prefix, self.suffix,
                                                      self.copy)
            self.update_list()
        except AttributeError as err_att:
            self.batch_renamer.logger.error(err_att)
            self.err_popup()
        except IndexError:
            self.batch_renamer.logger.error("Please include a file extension.")
            self.err_popup()
        else:
            self.complete_popup()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
 