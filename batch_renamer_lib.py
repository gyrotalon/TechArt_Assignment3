"""
Filename: batch_renamer_lib.py
Title: Batch File Renamer Library
Author: Macy Chantharak
Date Created: 2025-02-27
Date Edited: 2025-02-28
Description:
    This library contains a class with functions for renaming or copying files.
Python Version: 3.13
"""

import os
import logging
import shutil


class BatchRenamer:
    def __init__(self, 
                 filepath          = None,
                 copy_files        = False,
                 filetypes         = None,
                 strings_to_find   = None,
                 string_to_replace = '',
                 prefix            = None,
                 suffix            = None):
        self.filepath          = filepath
        self.copy_files        = copy_files
        self.filetypes         = filetypes
        self.strings_to_find   = strings_to_find
        self.string_to_replace = string_to_replace
        self.prefix            = prefix
        self.suffix            = suffix

        self.initialize_logger()


    def initialize_logger(self, print_to_screen = False):
        """
        Creates a logger

        Args:
            print_to_screen: for printing to screen as well as file
        """

        ###############
        # Basic Setup #
        ###############
        app_title = 'Test'
        version_number = '1.0.0'
        # get the path the script was run from, storing with forward slashes
        source_path = os.path.dirname(os.path.realpath(__file__))
        # create a log filepath
        logfile_name = f'{app_title}.log'
        logfile = os.path.join(source_path, logfile_name)

        # tell the user where the log file is
        print(f'Logfile is {logfile}')

        # more initialization
        self.logger = logging.getLogger(f'{app_title} Logger')
        self.logger.setLevel(logging.INFO)
        
        ###############################
        # Formatter and Handler Setup #
        ###############################
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)
        # formatting information we want (time, self.logger name, version, etc)
        formatter = logging.Formatter(f'%(asctime)s - %(name)s '
                                      f'{version_number} - '
                                      f'%(levelname)s - %(message)s')
        # setting the log file format
        file_handler.setFormatter(formatter)
        # clean up old handlers
        self.logger.handlers.clear()

        # add handler
        self.logger.addHandler(file_handler)

        # allowing to print to screen
        if print_to_screen:
            # create a new "stream handler" for logging/printing to screen
            console = logging.StreamHandler()
            self.logger.addHandler(console)
            # setting the print log format
            console.setFormatter(formatter)

        self.logger.info('Logger Initiated')


    def get_renamed_file_path(self, existing_name, string_to_find,
                              string_to_replace, prefix, suffix):
        """
        Returns the target file path given an existing file name and 
        string operations

        Args:
            existing_name: the existing file's name
            string_to_find: string to find and replace in the existing filename
            string_to_replace: the string you'd like to replace it with
            prefix: a string to insert at the beginning of the file path
            suffix: a string to append to the end of the file path
        """

        new_name = existing_name

        try:
            if (isinstance(string_to_find, str)):
                if string_to_find != '' and string_to_find in new_name:
                    new_name = new_name.replace(string_to_find, 
                                                string_to_replace)
            else:
                string_to_find = list(string_to_find)
                string_to_find.sort(reverse=True)
                for the_string in string_to_find:
                    if the_string != '' and the_string in new_name:
                        new_name = new_name.replace(the_string, 
                                                    string_to_replace)
            if prefix != '':
                new_name = prefix + new_name
            if suffix != '':
                name_only, ext = os.path.splitext(new_name)
                new_name = name_only + suffix + ext
            return new_name
        except TypeError:
            return

    def get_files_with_extension(self, folder_path, extension):
        """
        Returns a collection of files in a given folder with an extension that 
        matches the provided extension

        Args:
            folder_path: Path of the folder whose files you'd like to search
            extension: Extension of files you'd like to include in the return
        """

        files_with_extension_arr = []
        if extension[0] != '.':
            extension = '.' + extension
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            ext = os.path.splitext(file_name)[1]
            if (os.path.isfile(file_path) and ext == extension):
                files_with_extension_arr.append(file_name)
        return files_with_extension_arr

    def rename_file(self, existing_name, new_name, copy=False):
        """
        Renames a file if it exists
        By default, should move the file from its original path to 
        its new path-- removing the old file
        If copy is set to True, duplicate the file to the new path

        Args:
            existing_name: full filepath a file that should already exist
            new_name: full filepath for new name
            copy_mode: copy instead of rename
        """

        '''
        REMINDERS

        Copy files using shutil.copy
        make sure to import it at the top of the file
        '''
        self.logger.info('Attempting to ' + ('copy ' if copy else 'rename ') + 
                         f'{existing_name} to {new_name}')

        if os.path.isfile(existing_name):
            if not os.path.isfile(new_name):
                if copy:
                    shutil.copy(existing_name, new_name)
                    self.logger.info(f'Copied {existing_name} to {new_name}')
                else:
                    shutil.move(existing_name, new_name)
                    self.logger.info(f'Renamed {existing_name} to {new_name}')
            else:
                self.logger.error(f'{new_name} already exists '
                                  'and cannot be used as a new file name.')
        else:
            self.logger.error(f'File {existing_name} does not exist, ' 
                              'thus cannot be renamed.')

    def rename_files_in_folder(self, folder_path, extension, string_to_find,
                            string_to_replace, prefix, suffix, copy=False):
        """
        Renames all files in a folder with a given extension
        This should operate only on files with the provided extension
        Every instance of string_to_find in the filepath should be replaced
        with string_to_replace
        Prefix should be added to the front of the file name
        Suffix should be added to the end of the file name

        Args:
            folder_path: the path to the folder the renamed files are in
            extension: the extension of the files you'd like renamed
            string_to_find: the string in the filename you'd like to replace
            string_to_replace: the string you'd like to replace it with
            prefix: a string to insert at the beginning of the file path
            suffix: a string to append to the end of the file path
            copy: whether to rename/move the file or duplicate/copy it
        """

        self.logger.info('START: rename_files_in_folder will attempt to ' +  
                         ('copy ' if copy else 'rename ') + 
                         'files based on provided arguments.')
        if not copy:
            self.logger.warning('Renaming files may cause existing links '
                                'to break.')
        if(isinstance(extension, str)):
            if extension.count('.') >= 1 and extension[0] != '.':
                self.logger.warning('Multiple extensions are not supported.' 
                                    ' ABORTING.')
                return
        else:
            self.logger.warning('Extension input must be a string. ABORTING.')
            return

        if os.path.isdir(folder_path):
            self.logger.info(f'Opening {folder_path} to check for files.')
            existing_name_arr = self.get_files_with_extension(folder_path, 
                                                              extension)
            self.logger.info(f'Files with {extension} extension in ' 
                             f'{folder_path} are: {existing_name_arr}')
            for existing_name in existing_name_arr:
                new_name = self.get_renamed_file_path(existing_name, 
                                                      string_to_find, 
                                                      string_to_replace, 
                                                      prefix, suffix)
                if new_name != existing_name:
                    try:
                        new_name_path = os.path.join(folder_path, new_name)
                    except TypeError:
                        self.logger.error('string_to_replace, prefix, and ' 
                                          'suffix must be string type. ' 
                                          'string_to_find must be string ' 
                                          'or list/set/tuple of strings. ' 
                                          'ABORTING.')
                        return
                    existing_name_path = os.path.join(folder_path, 
                                                      existing_name)
                    self.rename_file(existing_name_path, new_name_path, copy)
        else:
            self.logger.error(f'The folder {folder_path} does not exist!')

        self.logger.info('END: rename_files_in_folder has finished running.')