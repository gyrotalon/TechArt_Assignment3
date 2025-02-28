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

    def get_parameters(self):
        self.extension = self.lineedit_extension.text()
        self.prefix = self.lineedit_prefix.text()
        self.suffix = self.lineedit_suffix.text()
        self.string_to_find = self.lineedit_string_to_find.text()
        self.string_to_replace = self.lineedit_string_to_replace.text()
        self.copy = self.button_copy.isChecked()

    def update_list(self):
        """
        Clear listwidget
        read files in filepath with os.walk
        Add files as new items
        """
        self.listWidget.clear()
        for root, dirs, files in os.walk(self.filepath):
            self.listWidget.addItems(files)


    # Add a function to gather and set parameters based upon UI
    # e.g. lineEdit.text() or radioButton.isChecked
    # remember that you may need to check to see if the result
    # was a tuple and correct like so:
    # self.filepath = self.filepathEdit.text()
    # if type(self.filepath) is tuple:
    #     self.filepath = self.filepath[0]

    def run_renamer(self):
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        """
        self.get_parameters()
        self.batch_renamer.rename_files_in_folder(self.filepath, 
                                                  self.extension, 
                                                  self.string_to_find,
                                                  self.string_to_replace,
                                                  self.prefix, self.suffix,
                                                  self.copy)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
 