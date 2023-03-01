# ------------------------------------------------- #
# Title: Assignment 07
# Description: Adds donation information to donationList by utilizing pickling and structured error handling
# ChangeLog: (Who, When, What)
# DTil, 03/01/2023, Created Script
# ------------------------------------------------- #


# Data ---------------------------------------------------------------------- #
import pickle

file_name_str = "donationList.dat"  # Name of the data file
donorInfo = {}  # A row of data separated into elements of a dictionary {Name, Donation}
donatorList = []  # list that acts as a table of rows


# Processing  --------------------------------------------------------------- #


class Processor:
    """  Performs Processing Tasks  """

    @staticmethod
    def write_data_to_file(file_name, list_of_rows):
        """  Write data from list of dictionary rows to file in binary

        :param file_name: (string) with name of file
        :param list_of_rows: (list) you want to save to file
        :return: nothing
        """
        objFile = open(file_name, "wb")  # open file to write in binary
        pickle.dump(list_of_rows, objFile)  # write entire list to file
        objFile.close()

    @staticmethod
    def read_data_from_file(file_name, list_of_rows):
        """  Reads binary data from file into list of dictionary rows

        :param file_name: (string) with name of file
        :param list_of_rows: (list) you want filled with file data
        :return: (list) of dictionary rows
        """
        list_of_rows = []  # Clears current data
        try:
            objFile = open(file_name, "rb")  # open file in binary format
        except FileNotFoundError:  # Exception if no file is found, typical for initial program start
            print("There is no existing donation list file.\n"
                  "Starting new file.")
            return list_of_rows  # return empty list

        tempfile = []  # temp list
        while True:
            try:
                tempfile = pickle.load(objFile)  # load all dictionary rows of data into temp list
                for row in tempfile:  # iterate through each dict in file
                    name, donation = row.values()
                    list_of_rows.append({"Name": str(name).title(), "Donation": int(donation)})  # add dict to list
            except pickle.UnpicklingError:  # Exception handling for non-binary file
                print("This file is not in binary format\n"
                      "Starting new file.")
                return list_of_rows  # return empty list
            except EOFError:  # Once all data is loaded, exception handle to return list
                print("Data has been uploaded from the file.")
                objFile.close()
                return list_of_rows

    @staticmethod
    def add_entry_to_list(donorName, donorValue, list_of_rows):
        """  Adds donor and donation to the list

        :param donorName: (string) with donor's full name
        :param donorValue: (int) with donation value
        :param list_of_rows: (list) you want to add more data to
        :return: (list) of dictionary rows
        """
        row = {"Name": str(donorName), "Donation": int(donorValue)}  # convert input info into dict object
        list_of_rows.append(row)  # add dictionary object to list
        print("%s has made a donation of $%i!\n" % (donorName, donorValue))
        return list_of_rows  # return list with new data


# Presentation (Input/Output)  -------------------------------------------- #

class IO:
    """  Performs Input and Output tasks"""

    @staticmethod
    def input_entry_name():
        """  Gets full name to be added to the list

        :return: (string) with name
        """
        while True:
            try:
                nameFirst = input("First name? ")  # User input first name
                if any(char == " " for char in nameFirst.strip()):  # for cases of entering whole name
                    raise Exception("Enter only the first name.")
                elif not nameFirst.strip().isalpha():  # exception for non-alphabetical input
                    raise Exception("Name must be of letters.")

                nameLast = input("Last name? ")  # User input last name
                if any(char == " " for char in nameLast.strip()):  # for cases of entering a space
                    raise Exception("Enter only the last name.")
                if not nameLast.strip().isalpha():  # exception for non-alphabetical input
                    raise Exception("Name must be of letters.")
                else:  # return whole name as single string if no exceptions
                    return (nameFirst.strip().capitalize() + " " + nameLast.strip().capitalize())
                    break
            except Exception as e:
                print(e)  # Print exception
            print()

    @staticmethod
    def input_entry_donation():
        """  Gets donation value to be added to the list

        :return: (int) of donation value
        """
        while True:
            try:
                donation = int(input("Enter donation amount - $"))  # User int input
            except ValueError as e:  # Exception for non numerical data
                print("Enter a valid whole dollar amount.")
            else:
                return donation  # return value if no exception
            print()

    @staticmethod
    def display_donator_list(list_of_rows):
        """  Shows current list in the list of dictionary rows

        :param list_of_rows: (list) of rows you want to display
        :return: nothing
        """
        print("\n******* The current donators are: *******")
        for row in list_of_rows:
            print(row["Name"] + " - $" + str(row["Donation"]))
        print("*******************************************")
        print()  # Add an extra line for looks

    @staticmethod
    def exit_option():
        """ Gets user input to continue or exit the program

        :return: Boolean
        """
        while True:
            try:
                exit = input("Add another donation? [Y/N] ")  # Prompt user input
                if not (exit.lower() == "y" or exit.lower() == "n"):  # Raise Exception if input is neither Y or N
                    raise Exception("Choose Y or N")
                elif exit.lower() == "n":  # Exit program prompt
                    IO.display_donator_list(donatorList)  # Display current list one last time
                    print("Thank you all for the donation!")
                    return True
                elif exit.lower() == "y":  # Continue program prompt
                    break
            except Exception as e:
                print(e)  # print exception
            print()
        return False


# Main Body of Script  ------------------------------------------------------ #


# When program starts, load datta from donationList.dat
donatorList = Processor.read_data_from_file(file_name=file_name_str, list_of_rows=donatorList)

while True:
    IO.display_donator_list(donatorList)  # displays current list

    name = IO.input_entry_name()  # gets name input from user
    donation = IO.input_entry_donation()  # gets donation input from user
    print()
    Processor.add_entry_to_list(donorName=name, donorValue=donation, list_of_rows=donatorList)  # Adds data to list

    Processor.write_data_to_file(file_name=file_name_str, list_of_rows=donatorList)  # Save data to file

    exit = IO.exit_option()  # Prompts to continue or exit program
    if exit == True:
        break

