# ------------------------------------------------- #
# Title: Lab7-1
# Description: A simple example of storing data in a binary file
# ChangeLog: (Who, When, What)
# <YourName>,<1.1.2030>,Created Script
# ------------------------------------------------- #
import pickle  # This imports code from another code file!

# Data -------------------------------------------- #
strFileName = 'AppData.dat'
lstCustomer = []

# Processing -------------------------------------- #
def save_data_to_file(file_name, list_of_data):
    file = open(file_name, "ab")
    pickle.dump(list_of_data, file)
    file.close()

def read_data_from_file(file_name):
    file = open(file_name, "rb")
    list_of_data = []
    while True:
        try:
            list_of_data.append(pickle.load(file))
        except:
            break
    file.close()
    return list_of_data

# Presentation ------------------------------------ #

intId = str(input("Enter an Id: "))
strName = str(input("Enter a Name: "))
lstCustomer = {'key': intId, 'val': strName}

save_data_to_file(strFileName, lstCustomer)

print(len(read_data_from_file(strFileName)))
counter = 0
for row in read_data_from_file(strFileName):
    key, val = row.values()
    try:
        print("This is %s and %s" % (key, val))
        counter += 1
    except:
        break
print()