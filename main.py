# Importing Pandas Library
import pandas as pd

# Creation of dataframe 'records' with column names as - VehRegNo, Age, Slot
# for storing information about parked Vehicles.
records = pd.DataFrame(columns=['VehRegNo', 'Age', 'Slot'])

# List to store availability of parking slots
# value 0 in list represents current slot is available, and 1 represents slot is occupied.
slots = []

# Checking the format of integer values.
# In FAQs it is given that all integer based entity will be in range 0-1000, (assuming that extremes are included).


def checkIntNoFormat(n):
    return 0 <= n <= 1000


# Checking the format of Registration Number to ensure it is valid or not.
# In FAQs it is given that length of registration numbers is 13, and they follow the format-> AA-DD-AA-DDDD
# where A depicts an Alphabet and D depicts an integer digit.


def checkRegNoFormat(regNo):
    if len(regNo
           ) == 13 and regNo[2] == '-' and regNo[5] == '-' and regNo[8] == '-':
        for i in [0, 1, 6, 7]:
            if 'A' <= regNo[i] <= 'Z':
                pass
            else:
                return False
        for i in [3, 4, 9, 10, 11, 12]:
            if 0 <= int(regNo[i]) <= 9:
                pass
            else:
                return False
        return True
    return False


# Creating parking lot of size 'n' mentioned in input file.
# Initializing the global list 'slots' with a list of size n, with all zeros.
# All zeroes represent that all slots are available initially


def createParkingLot(n):
    global slots
    slots = [0] * n
    print('Created parking of ' + str(n) + ' slots')


# Finds the available slot nearest to the entry.
# If all slots occuppied then returns -1 representing no available slots.


def findSlot():
    global slots
    for i in range(len(slots)):
        if slots[i] == 0:
            return i
    return -1


# Parks car with given registration number and marks the slot as occuppied(1) in the 'slots' list.
# Adds record of the parked car having information of its registration number, driver's age and slot number
# in the dataframe 'records'. If all slots are occuppied then it prints the message 'No slot available'


def parkCar(regNo, age):
    global records, slots
    slot = findSlot()
    if (slot == -1):
        print('No slot available')
        return
    slots[slot] = 1
    records = records.append({
        'VehRegNo': regNo,
        'Age': age,
        'Slot': slot
    },
                             ignore_index=True)
    print('Car with vehicle registration number "' + str(regNo) +
          '" has been parked at slot number ' + str(slot + 1))


# When a vehicle leaves its parking slot, this function makes the correspoding slot available
# by marking it 0, also removes the record of that car from the dataframe 'records'


def vactateSlot(slot):
    global records, slots
    slots[slot] = 0
    rec = records.loc[records['Slot'] == slot]
    regNo = rec['VehRegNo'].iloc[0]
    age = rec['Age'].iloc[0]
    records.drop(records[records['Slot'] == slot].index, inplace=True)
    print('Slot number ' + str(slot + 1) +
          ' vacated, the car with vehicle registration number "' + str(regNo) +
          '" left the space, the driver of the car was of age ' + str(age))


# Gets the slots of all vehicles from dataframe 'records'
# where driver's age is equal to given age


def slotForAge(age):
    global records
    slot_for_age = list(records.loc[records['Age'] == age]['Slot'])
    if len(slot_for_age) == 0:
        print()
        return
    for i in range(len(slot_for_age)):
        if i < len(slot_for_age) - 1:
            print(slot_for_age[i] + 1, end=',')
        else:
            print(slot_for_age[i] + 1)


# Gets the slots of all vehicles from dataframe 'records'
# where vehicle registration number is equal to given number


def slotForRegNo(regNo):
    global records
    slot_for_reg = list(records.loc[records['VehRegNo'] == regNo]['Slot'])
    if len(slot_for_reg) == 0:
        print()
        return
    print(slot_for_reg[0] + 1)


# Gets vehicle registration number of all vehicles from dataframe 'records'
# where driver's age is equal to given age


def regNoForDriverAge(age):
    global records
    reg_for_age = list(records.loc[records['Age'] == age]['VehRegNo'])
    if len(reg_for_age) == 0:
        print()
        return
    for i in range(len(reg_for_age)):
        if i < len(reg_for_age):
            print(reg_for_age[i], end=',')
        else:
            print(reg_for_age[i])


# This function will be called for every line/command in input file.
# Line will split into words separated by one or more whitespaces, words will get stored in 'words' list.
# Length of the words list is checked to check the format of command(whether all parameters and keywords are given or not)
# if yes, then only proceed further to run particular command.
# Keywords which describe the command are checked in the 'words' list, and function created for certain operation
# is called depending on the keyword found. If-else is used to check for different keywords and function calls.
# Parameters(stored as individual word in 'words' list) given in line/command will be passed to function.
# Assuming the format of commands will always be same, syntax checks for command are ignored,
# and parameters from line are extracted using hard-coded indices. (Parameters are stored in 'words' list)
# Also, checking the validity of registration number, age, slot using functions.


def mainFunc(line):

    global records, slots

    words = line.split()

    # Create Parking Lot
    if 'Create_parking_lot' in words and len(words) == 2:
        slotSize = int(words[-1])
        if checkIntNoFormat(slotSize):
            createParkingLot(slotSize)
        else:
            print('Invalid Input')

    # Park the car
    elif 'Park' in words and len(slots) and len(words) == 4:
        regNo = words[1]
        age = int(words[-1])
        if checkRegNoFormat(regNo) and checkIntNoFormat(age):
            parkCar(regNo, age)
        else:
            print('Invalid Input')

    # Vacate slot
    elif 'Leave' in words and len(slots) and len(records) and len(
            words) == 2 and 1 <= int(words[-1]) <= len(slots):
        slot = int(words[-1]) - 1
        if checkIntNoFormat(slot):
            vactateSlot(slot)
        else:
            print('Invalid Input')

    # Get Slot No for given driver's age
    elif 'Slot_numbers_for_driver_of_age' in words and len(slots) and len(
            words) == 2:
        age = int(words[-1])
        if checkIntNoFormat(age):
            slotForAge(age)
        else:
            print('Invalid Input')

    # Get Slot No for given Vehicle Registration Number
    elif 'Slot_number_for_car_with_number' in words and len(slots) and len(
            words) == 2:
        regNo = words[-1]
        if checkRegNoFormat(regNo):
            slotForRegNo(regNo)
        else:
            print('Invalid Input')

    # Get Vehicle Registration Number for given driver's age
    elif 'Vehicle_registration_number_for_driver_of_age' in words and len(
            slots) and len(words) == 2:
        age = int(words[-1])
        if checkIntNoFormat(age):
            regNoForDriverAge(age)
        else:
            print('Invalid Input')

    # Any other input will be invalid
    else:
        print('Invalid Input')


# Opening the input file in read mode and extracting every line/command one by one.
# mainFunc() is called for each line/command

if __name__ == "__main__":
    inputFile = open('input.txt', 'r')
    for line in inputFile:
        mainFunc(line)
