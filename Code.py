"""
######################### IMPORTED MODULE(S) #########################
"""
from columnar import columnar  # To present operations in form of a table

"""
######################### HELPER FUNCTIONS #########################
"""

"""
:Function Name: Flip_Bits
:Number of Parameters: 1
:Type of Parameters: string
:Return Type: string 
:Function Description: flip bits of binary number
"""


def Flip_Bits(String):  # One's complement of binary number
    """
    :param String: String containing binary equivalent of a number
    :return: String with the bits of the binary number flipped
    """
    flipped = ""

    for bit in String:
        if bit == '1':
            flipped += '0'  # Flip '1' to '0'
        else:
            flipped += '1'  # Flip '0' to '1'

    return flipped


"""
:Function Name: Equal_Bits
:Number of Parameters: 2
:Type of Parameters: string
:Return Type: string
:Function Description: returns the two entered numbers with same number of bits 
"""


def Equal_Bits(num1, num2):
    """
    :param num1: String containing binary equivalent of a number
    :param num2: String containing binary equivalent of a number
    :return: Two strings with equal number of bits
    """
    l1 = len(num1)
    l2 = len(num2)
    if l1 == l2:
        return num1, num2
    if l1 > l2:
        if num2[0] == '0':
            num2 = '0' * (l1 - l2) + num2
        else:
            num2 = '1' * (l1 - l2) + num2
    else:
        if num1[0] == '0':
            num1 = '0' * (l2 - l1) + num1
        else:
            num1 = '1' * (l2 - l1) + num1

    return num1, num2


"""
:Function Name: Bin_Add
:Number of Parameters: 2
:Type of Parameters: string
:Return Type: string
:Function Description: Adds two binary numbers
"""


def Bin_Add(num1, num2):
    """
    :param num1: String containing binary equivalent of a number
    :param num2: String containing binary equivalent of a number
    :return: String with sum/difference of two binary numbers [a + b]/[a + (-b)]
    """
    product = ""
    carry = "0"
    for i in range(len(num1) - 1, -1, -1):
        if carry == "0":
            if num1[i] == "0" and num2[i] == "0":  # 0 + 0 = 0
                product = "0" + product
            elif num1[i] == "1" and num2[i] == "1":  # 1 + 1 = 10  (carry =1)
                product = "0" + product
                carry = "1"
            else:
                product = "1" + product  # 0 + 1 = 1     &    1 + 0 = 1
        elif carry == "1":
            if num1[i] == "0" and num2[i] == "0":  # 1 (carry) 0 + 0 = 1
                product = "1" + product
                carry = "0"
            elif num1[i] == "1" and num2[i] == "1":  # 1 (carry) 1 + 1 = 11  (carry =1)
                product = "1" + product
                carry = "1"
            else:
                product = "0" + product  # 1 (carry) 0 + 1 = 10  &   1 (carry) 1 + 0 = 10
                carry = "1"

    """
    # Redundant!!

    if num1[0] == '1' and num2[0] == '1':
        return '1' + product
    if num1[0] == '0' and num2[0] == '0':
        if product[0] == '1':
            return '0' + product
    """
    return product


"""
:Function Name: Positive_Binary
:Number of Parameters: 1
:Type of Parameters: int
:Return Type: string 
:Function Description: convert a positive integer to binary form with sign bit
"""


def Positive_Binary(num):
    """
    :param num: An integer (only positive)
    :return: Binary equivalent with sign bit
    """
    bin_val = bin(num)[2:]
    bin_val = '0' + bin_val  # Sign bit for positive numbers is '0'
    return bin_val


"""
:Function Name: Twos_Complement
:Number of Parameters: 1
:Type of Parameters: int
:Return Type: string 
:Function Description: convert a negative (or positive) integer to its Two's complement representation 
"""


def Twos_Complement(num):
    """
    :param num: An integer (can be both positive or negative)
    :return: Two's complement representation of integer with sign bit
    """
    adj = abs(num + 1)  # Two's complement of -ve integer = one's complement of abs(integer + 1)
    s = bin(adj)[2:]
    comp = Flip_Bits(s)
    # Assign sign bit
    if num >= 0:
        comp = '0' + comp
    else:
        comp = '1' + comp

    return comp


"""
:Function Name: Convert_To_Binary
:Number of Parameters: 1
:Type of Parameters: int
:Return Type: string
:Function Description: A pseudo function used to distinguish between negative and positive numbers 
                       and call appropriate methods for binary conversion
"""


def Convert_To_Binary(num):
    """
    :param num: An integer
    :return: String containing binary equivalent of integer with sign bit
    """
    if num >= 0:
        return Positive_Binary(num)  # Call for positive integer
    else:
        return Twos_Complement(num)  # Call for negative integer


"""
:Function Name: Arithmetic_Right_Shift
:Number of Parameters: 0
:Type of Parameters: -
:Return Type: list 
:Function Description: perform arithmetic right shift on AC , QR and Qn
"""


def Arithmetic_Right_Shift():
    """
    :return: A list of arithmetically right shifted accumulator, multiplier and Qn
    """
    global Acc, Q, qr

    temp = Acc[0]
    qr = Q[-1]
    Q = Acc[-1] + Q[:-1]
    Acc = temp + Acc[:-1]

    return [Acc, Q, qr]


"""
:Function Name: Perform_Operation
:Number of Parameters: 0
:Type of Parameters: -
:Return Type: list 
:Function Description: performs appropriate operation based on 'QR(LSB)' + 'Qn'
"""


def Perform_Operation():
    """
    :return: A list containing Accumulator, multiplier and Qn after appropriate operation
    """
    global Acc, M, Q, qr, Mtw
    Op = Q[-1] + qr

    if Op == "00" or Op == "11":
        '''
            If 00 or 11 : Just arithmetic right shift
        '''
        ARS = Arithmetic_Right_Shift()
        return ARS
    elif Op == "01":
        '''
            If 01 : AC = AC + M
                    then, arithmetic right shift
        '''
        Acc = Bin_Add(Acc, M)
        ARS = Arithmetic_Right_Shift()
        return ARS
    elif Op == "10":
        '''
            If 10 : AC = AC - M   (Mtw = -M)
                    then, arithmetic right shift
        '''
        Acc = Bin_Add(Acc, Mtw)
        ARS = Arithmetic_Right_Shift()
        return ARS
    else:
        print("An error occurred: Operation not recognised!")
        return []


"""
######################### MAIN ALGORITHM #########################
"""

"""
:Function Name: Booth_Algorithm
:Number of Parameters: 0 
:Type of Parameters: -
:Return Type: - 
:Function Description: performs Booth's algorithm for binary multiplication
"""


def Booth_Algorithm():
    """
    :return: Nothing
    """
    global output, Acc, M, Q, qr, Mtw
    Sc = len(M)  # Number of operations = number of bits

    Acc, M = Equal_Bits(Acc, M)
    output.append([Acc, Q, qr, Sc])  # Initial state after all inputs
    for i in range(Sc):  # Run loop till required number of operations completed
        p = Perform_Operation()
        p.append(Sc - i - 1)
        output.append(p)  # Append each line to output list
    return


"""
######################### GLOBAL VARIABLES #########################
"""
output = []  # Empty list to store output
Acc, qr = '0', '0'  # Set accumulator and Qn to '0'

"""
######################### MAIN CODE #########################
"""
a = int(input("Enter multiplicand: "))  # Input multiplicand i.e. integer to be multiplied
b = int(input("Enter multiplier: "))  # Input multiplier i.e. integer by which to multiply

M = Convert_To_Binary(a)  # Binary of multiplicand
Q = Convert_To_Binary(b)  # Binary of multiplier
Mtw = Convert_To_Binary(a * -1)  # Store value of -M

# To make sure that operands hold equal number of bits
M, Q = Equal_Bits(M, Q)
Q, Mtw = Equal_Bits(Q, Mtw)

# To check values
print('\n M =', M)
print(' Q =', Q)
print('-M =', Mtw)

Booth_Algorithm()  # Call to the main algorithm

# Create table
"""
TABLE CONTENTS:
AC: Accumulator
QR: Multiplier
Qn: Extra single bit register
SC: Number of operations left
"""
headers = ["AC", "QR", "Qn", "SC"]
table = columnar(output, headers, no_borders=True)
print(table)

# In case required module not available
# for i in output:
#    print(i)

res = Acc + Q  # Product is AC + QR

if res[0] == '0':  # Print final result if positive
    print("Final result :")
    print("AC + QR =", res)
    print("Product = ", int('0b' + res, 2))
else:  # Convert to Two's complement if final result is negative
    one = '01'
    res, one = Equal_Bits(res, one)
    res1 = Flip_Bits(res)
    res1 = Bin_Add(res1, one)
    print("Final result : ")
    print("AC + QR =", res, '=', '-' + res1)
    print("Product =", '-' + str(int('0b' + res1, 2)))

"""
######################### END OF PROGRAM #########################
"""
