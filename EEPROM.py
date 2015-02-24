import os, sys
print "Welcome to the EEPROM python script for reading/writing and erasing."

while (True):
    
    print "1) Read"
    print "2) Write"
    print "3) Erase"
    print "4) Abort"
    answer = raw_input("Please make your selection:")
    
    if (answer=="1"):
        print "1"
        os.system("sudo python EEPROMr.py")
    if (answer=="2"):
        print "2"
        os.system("sudo python EEPROMw.py")
    if (answer=="3"):
        print "3"
        os.system("sudo python EEPROMd.py")
    if (answer=="4"):
        print "Aborting"
        sys.exit()
    else:
        print "Please select one of the options"
