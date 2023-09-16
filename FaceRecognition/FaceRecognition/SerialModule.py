import serial
import time

def initConnection(portNo, baudrate):
    try:
        ser = serial.Serial(portNo, baudrate)
        print('Device Connected')
        return ser
    except:
        print('Not Connected')

def sendData(serial, data, digitPerValueReceived):
    myString = '$'
    for d in data:
        myString += str(d).zfill(digitPerValueReceived) # zfill will add 0 before data, for example: data is 50 => 050
    try:
        serial.write(myString.encode())
        print(myString)
    except:
        print('Data transmission Failed')



# if __name__ == '__main__':
#     ser = initConnection('/dev/ttyACM0', 9600)
#     while True:
#         sendData(ser, [50, 255], 3)
#         time.sleep(1)
#         sendData(ser, [0, 0], 3)
#         time.sleep(1)