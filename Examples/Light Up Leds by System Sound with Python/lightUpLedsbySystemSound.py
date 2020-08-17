import time, os, datetime, random, serial, subprocess

#set connection port
port = 'COM3'
#set connection velocity
velocity = 9600

print('Connecting to Arduino...')
arduino = serial.Serial(port, velocity)
time.sleep(3)

# hold actual time for timer function
oldTime = datetime.datetime.now()

# set timer function
def timer(seconds):
    if (datetime.datetime.now() - oldTime).total_seconds() > seconds: return True
    return False


cmd = 'meters.exe'
def getVolumePeak():      
    try:  
        output = subprocess.check_output (cmd).decode('utf-8')
        splitedOutput = output.split('\n\r')
        peak = float(splitedOutput[0].split('Mute')[0].split('Peak: ')[1])
        return peak
    except:
        return 0

maxPeak = 0
def peakToLeds(totalOfLeds):
    global maxPeak
    peak = getVolumePeak()

    if peak == 0:
        return '{};'.format('0' * totalOfLeds) 

    if maxPeak < peak: maxPeak = peak

    
    actualPeakFraction = peak/maxPeak

    numberOfLedsToLightUp = int(totalOfLeds * actualPeakFraction)

    stringToArduino = ''

    for x in range(numberOfLedsToLightUp):
        stringToArduino += '1'
    
    for x in range(totalOfLeds - numberOfLedsToLightUp):
        stringToArduino += '0'

    return '{};'.format(stringToArduino)
    # maxPeak = 100%
    # totalOfLeds = 100%

       

while True:
    # send message to Arduino
    arduino.write(peakToLeds(10).encode())

    # read output from Arduino and print it
    #arduinoOutput = arduino.readline().decode('utf-8').replace('\n','')
    #print(datetime.datetime.now(), arduinoOutput)

    #if (timer(10)):
    #    maxPeak = 0

    # clean input and output data
    arduino.flushInput()
    #arduino.flushOutput()

    # add 100ms delay