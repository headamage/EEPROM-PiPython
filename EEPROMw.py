import RPi.GPIO as GPIO
import time, re
GPIO.setmode(GPIO.BCM) #Use chip numbering scheme

#CE, WE, OE pins (pull down to activate each mode):
GPIO.setup (2, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #CE
GPIO.setup (3, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #OE
GPIO.setup (4, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #WE

#Set the chip in standby mode while setting up the rest GPIO:
GPIO.output(2,1) #CE - high
GPIO.output(3,1) #OE - high
GPIO.output(4,1) #WE - high

#Address pins set for output (A15, A16, A17 connected to ground):
GPIO.setup (10, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A0
GPIO.setup (9,  GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A1
GPIO.setup (11, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A2
GPIO.setup (25, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A3
GPIO.setup (8,  GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A4
GPIO.setup (7,  GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A5
GPIO.setup (5,  GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A6
GPIO.setup (6,  GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A7
GPIO.setup (12, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A8
GPIO.setup (13, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A9
GPIO.setup (19, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A10
GPIO.setup (26, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A11
GPIO.setup (16, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A12
GPIO.setup (20, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A13
GPIO.setup (21, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #A14

#Data pins set for output (pull down for zeroes):
GPIO.setup (14, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D0
GPIO.setup (15, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D1
GPIO.setup (18, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D2
GPIO.setup (17, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D3
GPIO.setup (27, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D4
GPIO.setup (22, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D5
GPIO.setup (23, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D6
GPIO.setup (24, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) #D7

j=0
while (j==0):
    A=[]
    A=raw_input("Type memory address (15 bits): ")

    if not re.match("^[0-1]*$", A) or (len(A) != 15):
        print "Error! Only 1 and 0 allowed. Please type 15 bits."
    else:
        j=1
        A=map(int, A)
        
i=0
while (i==0):
    D=[]
    D=raw_input("Type data byte: ")

    if not re.match("^[0-1]*$", D) or (len(D) !=8):
        print "Error! Only 1 and 0 allowed. Please type 8 bits"
    else:
        i=1
        D=map(int, D)

print"Are you sure you wish to write to the chip?(Y/n):"
answer=raw_input()

#Operation Loop
try:

    if (answer=="y" or answer=="Y"):
        print "Turning on the chip."
        GPIO.output(2,0) #CE - low - turn on the chip
        time.sleep(0.1)
        print "Starting chip programming sequence."

        #First sequence of software protection:
        print "Step 1: A=0x5555 - D=0xAA"
        #set address bus to 0x5555:
        GPIO.output(10,1) #D0
        GPIO.output(9, 0) #D1
        GPIO.output(11,1) #D2
        GPIO.output(25,0) #D3
        GPIO.output(8, 1) #D4
        GPIO.output(7, 0) #D5
        GPIO.output(5, 1) #D6
        GPIO.output(6, 0) #D7
        GPIO.output(12,1) #D8
        GPIO.output(13,0) #D9
        GPIO.output(19,1) #D10
        GPIO.output(26,0) #D11
        GPIO.output(16,1) #D12
        GPIO.output(20,0) #D13
        GPIO.output(21,1) #D14
        GPIO.output(4, 0) #WE - low - latched address
        print "Address latched."

        #Set data bus to 0xAA:
        GPIO.output(14,0)
        GPIO.output(15,1)
        GPIO.output(18,0)
        GPIO.output(17,1)
        GPIO.output(27,0)
        GPIO.output(22,1)
        GPIO.output(23,0)
        GPIO.output(24,1)
        GPIO.output(4, 1) #WE - high - latched data
        print "Data latched."

        #Second sequence of software protection:
        print "Step 2: A=0x2AAA - D=0x55"
        #set address bus to 0x2AAA:
        GPIO.output(10,0)
        GPIO.output(9, 1)
        GPIO.output(11,0)
        GPIO.output(25,1)
        GPIO.output(8, 0)
        GPIO.output(7, 1)
        GPIO.output(5, 0)
        GPIO.output(6, 1)
        GPIO.output(12,0)
        GPIO.output(13,1)
        GPIO.output(19,0)
        GPIO.output(26,1)
        GPIO.output(16,0)
        GPIO.output(20,1)
        GPIO.output(21,0)
        GPIO.output(4,0) #WE - low - latched address
        print "Address latched."

        #Set data bus to 0x55:
        GPIO.output(14,1)
        GPIO.output(15,0)
        GPIO.output(18,1)
        GPIO.output(17,0)
        GPIO.output(27,1)
        GPIO.output(22,0)
        GPIO.output(23,1)
        GPIO.output(24,0)
        GPIO.output(4,1) #WE - high - latched data
        print "Data latched."

        #Third sequence of software protection:
        print "Step 3: A=0x5555 - D=0xA0"
        #set address bus 0x5555:
        GPIO.output(10,1)
        GPIO.output(9, 0)
        GPIO.output(11,1)
        GPIO.output(25,0)
        GPIO.output(8, 1)
        GPIO.output(7, 0)
        GPIO.output(5, 1)
        GPIO.output(6, 0)
        GPIO.output(12,1)
        GPIO.output(13,0)
        GPIO.output(19,1)
        GPIO.output(26,0)
        GPIO.output(16,1)
        GPIO.output(20,0)
        GPIO.output(21,1)
        GPIO.output(4,0) #WE - low - latched address
        print "Address latched."

        #Set data bus to 0xA0:
        GPIO.output(14,0)
        GPIO.output(15,0)
        GPIO.output(18,0)
        GPIO.output(17,0)
        GPIO.output(27,0)
        GPIO.output(22,1)
        GPIO.output(23,0)
        GPIO.output(24,1)
        GPIO.output(4,1) #WE - high - latched data
        print "Data latched."

        #Actual write operation:
        print "Writing user data to selected address."
        #Set address bus:
        GPIO.output(10,A[0])
        GPIO.output(9,A[1])
        GPIO.output(11,A[2])
        GPIO.output(25,A[3])
        GPIO.output(8,A[4])
        GPIO.output(7,A[5])
        GPIO.output(5,A[6])
        GPIO.output(6,A[7])
        GPIO.output(12,A[8])
        GPIO.output(13,A[9])
        GPIO.output(19,A[10])
        GPIO.output(26,A[11])
        GPIO.output(16,A[12])
        GPIO.output(20,A[13])
        GPIO.output(21,A[14])
        GPIO.output(4,0) #WE - low - latched address
        print "User address latched."

        #Set data bus:
        GPIO.output(14,D[0])
        GPIO.output(15,D[1])
        GPIO.output(18,D[2])
        GPIO.output(17,D[3])
        GPIO.output(27,D[4])
        GPIO.output(22,D[5])
        GPIO.output(23,D[6])
        GPIO.output(24,D[7])
        GPIO.output(4,1) #WE - high - latched data
        print "User data latched."

        GPIO.output(2,1) #CE - high - standby chip
        print "Chip on standby."
        time.sleep(0.1)
        GPIO.cleanup()
        print "Performing GPIO cleanup.\nOperation Completed."

    else:
        print "Operation Aborted.\nPerforming GPIO cleanup."
        GPIO.cleanup()

except KeyboardInterrupt:
    print "Keyboard Interrupt.\nPerforming GPIO cleanup."
    GPIO.cleanup()
