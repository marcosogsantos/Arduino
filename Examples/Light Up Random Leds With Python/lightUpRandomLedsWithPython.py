import time, os, datetime, random, serial

#set connection port
port = 'COM3'
#set connection velocity
velocity = 9600

print('Connecting to Arduino...')
arduino = serial.Serial(port, velocity)
time.sleep(3)

# set message randomizer
def randomMessage(length):
    output = ''
    for x in range(length):
        output += random.choice(['0','1'])
    return output

# hold actual time for timer function
oldTime = datetime.datetime.now()

# set timer function
def timer(seconds):
    if (datetime.datetime.now() - oldTime).total_seconds() > seconds: return True
    return False

# set first random message to send
arduinoInput = "{};".format(randomMessage(5)).encode()

while True:
    # send message to Arduino
    arduino.write(arduinoInput)

    # read output from Arduino and print it
    arduinoOutput = arduino.readline().decode('utf-8').replace('\n','')
    print(datetime.datetime.now(), arduinoOutput)

    # check if message is complete
    if ";" in arduinoOutput:
        # clean input and output data
        arduino.flushInput()
        arduino.flushOutput()

    # check if passed 1 second since last random message setup
    if (timer(1)):

        # set a new random message
        arduinoInput = "{};".format(randomMessage(5)).encode()
        
        # reset timer
        oldTime = datetime.datetime.now()

    # add 100ms delay
    time.sleep(.1)