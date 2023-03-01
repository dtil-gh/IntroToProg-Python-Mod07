# Donation List Python Script
**Dev:** *DTil*  
**Date:** *03.01.2023*  
*IT FDN 100 A*  
*Assignment 07*  

## Introduction
In this assignment, I will utilize the lessons learned about pickling and exception handling to build a python script that will read a binary file that contains donation information regarding the name of donor and donation amount and write additional information in binary to the file. Similarly, to previous assignment, I will use classes and functions to operate this script.

## Main Body of Script and Declared Variables
Before diving deep into the script, the main body of script shows the order of operations for how I want my script to follow. (Figure 2) Simply, I want to read the data, then display the data, then input new information to be saved to the file, then prompt to continue or end program. 

```
# Data ---------------------------------------------------------------------- #
import pickle

file_name_str = "donationList.dat"  # Name of the data file
donorInfo = {}  # A row of data separated into elements of a dictionary {Name, Donation}
donatorList = []  # list that acts as a table of rows
```
#### Figure 1: Declared Variables

```
# When program starts, load data from donationList.dat
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
```
#### Figure 2: Body of Script

## Read Data from Binary File
First step is to load the data located in Processing class. For first time users, the file declared in Figure 1 may not exist. I have written an exception to start a new list which will be saved in binary in a later function. (Figure 3)

```
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
```
#### Figure 3: Read Data from File Function, Error Handling for First Time Users

For when the file does exist, there may be a chance that the file is not in binary format or corrupted in some way. For those cases, I will start a new list that will be later overwritten to the donationList.dat file as seen in line 47-49. (Figure 4) 

```
tempfile = []  # temp list
try:
    tempfile = pickle.load(objFile)  # load a dictionary row of data into temp list
    for row in tempfile:  # iterate through each dict in file
        name, donation = row.values()
        list_of_rows.append({"Name": str(name).title(), "Donation": int(donation)})  # add dict to list
    objFile.close()
    print("Data has been uploaded from the file.")
except pickle.UnpicklingError:  # Exception handling for non-binary file
    print("This file is not in binary format\n"
          "Starting new file.")
return list_of_rows
```
#### Figure 4: Read Data from File Function, Error Handling for Non-Binary Formatted File

Displaying the current list is similarly written to a function shown in a previous assignment but I have rewritten the display text to fit my script. (Figure 5) This can be found in the Input/Output class.

```
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
```
#### Figure 5: Display List Function

## Adding Entry to List
Now that I have loaded and converted the binary data to a list variable, I will have the user add information regarding a new donation, their full name and donation amount. The user will be first prompted to provide a full name with first and last name in separate inputs. (Figure 6) I have written a separate input function for both first and last name to handle when either first or last name input raises an exception, it will prompt the user for the information that the exception came from. For both first and last name input, I have handled errors for non-alphabetical strings with an “if not .isalpha()” statement. In case for those that might prematurely enter the full name in the first input, I raised an exception to let the user know that the program is asking for just the first name. (lines 94 and 107) Also included similar code with last name input. Once all information given raises no exceptions, I returned concatenated both strings in a proper full name format. (line 10)

```
@staticmethod
def input_entry_name():
    """  Gets full name to be added to the list

    :return: (string) with name
    """
    # Exception Handling for First Name Input
    while True:
        try:
            nameFirst = input("First name? ")  # User input first name
            if any(char == " " for char in nameFirst.strip()):  # for cases of entering whole name
                raise Exception("Enter only the first name.")
            elif not nameFirst.strip().isalpha():  # exception for non-alphabetical input
                raise Exception("First name must be of letters.")
        except Exception as e:
            print(e)  # Print exception
        else:
            break
        print()
    # Exception Handling for Last name Input
    while True:
        try:
            nameLast = input("Last name? ")  # User input last name
            if any(char == " " for char in nameLast.strip()):  # for cases of entering a space
                raise Exception("Enter only the last name.")
            if not nameLast.strip().isalpha():  # exception for non-alphabetical input
                raise Exception("Last name must be of letters.")
            else:  # return whole name as single string if no exceptions
                return (nameFirst.strip().capitalize() + " " + nameLast.strip().capitalize())
        except Exception as e:
            print(e)  # Print exception
        print()
``` 
#### Figure 6: Input Name Function

After the user inputs a full name, the user will then input an value for donation amount. Since I have written int(input()), the only error that can come about is when it is not possible to convert the string input to an integer object. This will give a ValueError exception. (Figure 7)

```
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
```
#### Figure 7: Input Donation Amount Function

Now that both of the input functions above have return a string for the full name and an integer for the donation amount, I will include them in as arguments to add them to the list. (Figure 8) This function is simple as it is appending the information to the existing list of dictionaries. No error can come from this since the arguments are of string and integer type which are already handled in the input functions above.

```
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
```
#### Figure 8: Adding Donor Information to List Function

## Writing Data to File as Binary
Now that the list has been updated with a new donor information, I can write the list to the file as binary with a dump() function. I have set the open mode to “wb” since it will handle cases where the file does not exist. (Figure 9)

```
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

```
#### Figure 9: Writing Data as Binary to File

## Exit Prompt
With the file overwritten or made with new information, I will prompt the user to either continue or end the program. (Figure 10) I made a function for this exiting option since it involves input which can lead to errors. With a specific condition noted in line 147, the only error that can come from this is when the user inputs a value that’s neither of the options from the prompt. Doing so will repeat the prompt to the user again to state clearly Y or N. 

```
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
```
#### Figure 10: Exiting Function

## Testing Script
I will test the script in PyCharm with no existing file. (Figure 11) In this test, I will also include how various inputs for name input and donation. As we can see in Figure 12, the file is in binary form as it cannot be humanly read.

![Testing Script in PyCharm](https://github.com/dtil-gh/IntroToProg-Python-Mod07/blob/main/docs/Figure11.png "Testing Script in PyCharm")
#### Figure 11: Testing Script in PyCharm 

![PyCharm Binary File Input](https://github.com/dtil-gh/IntroToProg-Python-Mod07/blob/main/docs/Figure12.png "PyCharm Binary File Output")
#### Figure 12: PyCharm Binary File Output

For Command Shell testing, I will use the binary file that was created from the above PyCharm test and perform similar inputs to see how the script handles errors. (Figure 13) As we can see from Figure 14, it has changed from Figure 12 due to my test run in Shell. Running the program again, we can see that the binary file is being loaded correctly. (Figure 15)

![Testing Script in Command Shell](https://github.com/dtil-gh/IntroToProg-Python-Mod07/blob/main/docs/Figure13.png "Testing Script in Command Shell")
#### Figure 13: Testing Script in Command Shell

![Shell Binary File Output](https://github.com/dtil-gh/IntroToProg-Python-Mod07/blob/main/docs/Figure14.png "Shell Binary File Output") 
#### Figure 14: Shell Binary File Output

![Running Script to Verify Change](https://github.com/dtil-gh/IntroToProg-Python-Mod07/blob/main/docs/Figure15.png "Running Script to Verify Change") 
#### Figure 15: Running Script to Verify Change 

## Conclusion
In this module, I learned how to further develop my skills in classes and functions following the previous assignment but also incorporated pickling and error handling. The challenging part about pickling is creating a code that can properly extract the binary information to be saved as a list of dictionaries in my code. As for error handling, there can be a vast amount of errors that can arise from having user input involved. For future updates to the script, I would create classes to hold information for all custom errors I’ve created and if possible, reduce the amount of redundancy as seen in “input_entry_name()”.
