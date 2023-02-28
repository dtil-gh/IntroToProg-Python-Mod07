# ---------------------------------------------------------------------------- #
# Title: Assignment 06
# Description: Working with functions in a class,
#              When the program starts, load each "row" of data
#              in "ToDoToDoList.txt" into a python Dictionary.
#              Add the each dictionary "row" to a python list "table"
# ChangeLog (Who,When,What):
# RRoot,1.1.2030,Created started script
# DTil, 2.22.2023, Modified code to complete assignment 06
# ---------------------------------------------------------------------------- #

import pickle

# Data ---------------------------------------------------------------------- #
# Declare variables and constants
file_obj = None  # An object that represents a file
row_dic = {}  # A row of data separated into elements of a dictionary {Task,Priority}
table_lst = []  # A list that acts as a 'table' of rows
choice_str = ""  # Captures the user option selection


# Processing  --------------------------------------------------------------- #
class Processor:
    """  Performs Processing tasks """

    @staticmethod
    def read_data_from_file(file_name, list_of_rows):
        """ Reads data from a file into a list of dictionary rows

        :param file_name: (string) with name of file:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of dictionary rows
        """
        list_of_rows = []  # clear current data
        if file_name != None:
            file = open(file_name, "rb")
            tempfile = []
            while True:
                try:
                    tempfile.append(pickle.load(file))
                except EOFError:
                    break
                except pickle.UnpicklingError as e:
                    print("This file was not saved in binary format!\n")
                    return e

            for row in tempfile:
                task, priority = row.values()
                row = {"Task": str(task), "Priority": str(priority)}
                list_of_rows.append(row)
            file.close()
        else:
            print("Creating new ToDO List!")
        return list_of_rows

    @staticmethod
    def add_data_to_list(task, priority, list_of_rows):
        """ Adds data to a list of dictionary rows

        :param task: (string) with name of task:
        :param priority: (string) with name of priority:
        :param list_of_rows: (list) you want to add more data to:
        :return: (list) of dictionary rows
        """
        # Checks if Task exists in list
        for checkRow in list_of_rows:
            taskname, val = dict(checkRow).values()
            if taskname.lower() == task.lower():
                print("'%s' is already in the list!" % task.capitalize())  # Prompts user that task exist
                return list_of_rows  # Return list with no duplicate

        #  If there are no duplicate task, then add task to list
        row = {"Task": str(task).strip(), "Priority": str(priority).strip()}
        list_of_rows.append(row)  # Append new dict to existing list
        print("Added '%s' with %s priority to the list!" % (task.lower(), priority.lower()))
        return list_of_rows  # Return list with new task

    @staticmethod
    def remove_data_from_list(task, list_of_rows):
        """ Removes data from a list of dictionary rows

        :param task: (string) with name of task:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of dictionary rows
        """

        for row in list_of_rows:   # Iterate through list to find task to be removed
            taskName, prioName = dict(row).values()
            if taskName.lower() == task.lower():
                list_of_rows.remove(row)  # Remove dictionary from list if task is found
                print("'%s' has been deleted from the list!" % task.capitalize())
                return list_of_rows  # returns updated list without the task to be removed
        print("'%s' cannot be removed from list as it does not exist." % task.capitalize())
        return list_of_rows  # returns same list

    @staticmethod
    def write_data_to_file(file_name, list_of_rows):
        """ Writes data from a list of dictionary rows to a File

        :param file_name: (string) with name of file:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of dictionary rows
        """
        file = open(file_name, "wb")
        for dict in list_of_rows:
            pickle.dump(dict, file)
        file.close()

        return list_of_rows


# Presentation (Input/Output)  -------------------------------------------- #


class IO:
    """ Performs Input and Output tasks """

    @staticmethod
    def output_menu_tasks():
        """  Display a menu of choices to the user

        :return: nothing
        """
        print('''
        Menu of Options
        1) Add a new Task
        2) Remove an existing Task
        3) Save Data to New or Existing File        
        4) Exit Program
        ''')
        print()  # Add an extra line for looks

    @staticmethod
    def input_menu_choice():
        """ Gets the menu choice from a user

        :return: string
        """
        try:
            choice = str(input("Which option would you like to perform? [1 to 4] - ")).strip()
            if not choice.isnumeric():
                raise Exception("Use numbers to choose a menu option")
        except Exception as e:
            print("There was an error!")
        print()  # Add an extra line for looks
        return choice

    @staticmethod
    def output_current_tasks_in_list(list_of_rows):
        """ Shows the current Tasks in the list of dictionaries rows

        :param list_of_rows: (list) of rows you want to display
        :return: nothing
        """
        print("\n******* The current tasks ToDo are: *******")
        for row in list_of_rows:
            print(row["Task"] + " (" + row["Priority"] + ")")
        print("*******************************************")
        print()  # Add an extra line for looks

    @staticmethod
    def input_new_task_and_priority():
        """  Gets task and priority values to be added to the list

        :return: (string, string) with task and priority
        """
        taskName = input("What is the name of the task you would like to add? ")
        prioName = input("What's the priority of this task? [Low, Medium, High] - ")
        return taskName, prioName  # Returns task and priority data given by user

    @staticmethod
    def input_task_to_remove():
        """  Gets the task name to be removed from the list

        :return: (string) with task
        """
        remTask = input("What is the name of the task you would like to remove? ")
        return remTask  # Returns task name that user wants to remove

    @staticmethod
    def input_file_to_load():
        """  Gets file name to load from

        :return: (string) with name of file in .dat format
        """
        while True:
            try:
                fileName = input("Please type in the .dat file to be loaded or type \"new\" to create new list. ")
                if fileName.endswith(".dat") == True:
                    return fileName
                elif fileName.lower() == "new":
                    return None
                else:
                    raise FileNotDATError()
            except FileNotFoundError as e:
                print("File is not found, please check your spelling.")
            except Exception as e:
                print(e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def input_file_to_save(file_name):
        """  Gets file name to save to

        :return: (string) with name of file in .dat format
        """
        while True:
            try:
                print('''
                Would you like to overwrite existing file or save to new file?
                    1 - Overwrite Existing
                    2 - Save to New
                ''')
                fileChoice = int(input("[1 or 2] "))
                if fileChoice == 1:
                    return file_name
                elif fileChoice == 2:
                    fileName = input("What is the name of the new file you would like to save to? ")
                    if fileName.endswith(".dat") == True:
                        return fileName
                    else:
                        raise FileNotDATError
                elif fileChoice != 1 or fileChoice != 2:
                    raise Exception("Type either 1 or 2 as an option.")
            except Exception as e:
                print(e, e.__doc__, type(e), sep='\n')


class FileNotDATError():
    """  File extension must end with .dat to indicate it is a binary file  """
    def __str__(self):
        return "File extension is not .dat"


# Main Body of Script  ------------------------------------------------------ #


# Step 1 - When the program starts, Load data from ToDoFile.txt.
while True:
    file_name_load = IO.input_file_to_load()
    table_lst = Processor.read_data_from_file( file_name=file_name_load, list_of_rows=table_lst)  # read file data
    if type(table_lst) != list:
        print("Please load a binary file!\n")
    else:
        break

# Step 2 - Display a menu of choices to the user
while (True):
    # Step 3 Show current data
    IO.output_current_tasks_in_list(list_of_rows=table_lst)  # Show current data in the list/table
    IO.output_menu_tasks()  # Shows menu
    choice_str = IO.input_menu_choice()  # Get menu option

    # Step 4 - Process user's menu choice
    if choice_str.strip() == '1':  # Add a new Task
        task, priority = IO.input_new_task_and_priority()
        table_lst = Processor.add_data_to_list(task=task, priority=priority, list_of_rows=table_lst)
        continue  # to show the menu

    elif choice_str == '2':  # Remove an existing Task
        task = IO.input_task_to_remove()
        table_lst = Processor.remove_data_from_list(task=task, list_of_rows=table_lst)
        continue  # to show the menu

    elif choice_str == '3':  # Save Data to File
        file_name_save = IO.input_file_to_save(file_name_load)
        print(file_name_save)
        table_lst = Processor.write_data_to_file(file_name=file_name_save, list_of_rows=table_lst)
        print("Data Saved!")
        continue  # to show the menu

    elif choice_str == '4':  # Exit Program
        print("Goodbye!")
        break  # by exiting loop
