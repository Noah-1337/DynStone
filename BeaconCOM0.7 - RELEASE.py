from ntpath import join
import tkinter
from turtle import width
import serial
import time
from tkinter import *
from tkinter.ttk import *
import serial
import serial.tools.list_ports


def GUIreceive():
    #Deleting previously created window for selection
    root.destroy()

    #Clearing labels which could contain old information if executed repeatedly
    def destroylabel():
        field100_label.destroy()
        field200_label.destroy()
        field300_label.destroy()
        field10_label.destroy()
        field20_label.destroy()
        field30_label.destroy()

    def ablesen():
        #Defining a variable for the serial port
        COMPORT = clicked.get()
        
        #Connecting to serial port chosen by the user and reading the last three lines (must be three to work with the .ino)
        arduino = serial.Serial(COMPORT, baudrate = 115200)
        arduino_bytes1 = str(arduino.readline())
        arduino_bytes2 = str(arduino.readline())
        arduino_bytes3 = str(arduino.readline())
        
        destroylabel()
        
        #Checking if the char sequence "is" can be found and storing it for further processing(should be in exactly one of the three provided strings)
        foundin = str(0)
        if "is" in arduino_bytes1:
            foundin = arduino_bytes1
            

        if "is" in arduino_bytes2:
            foundin = arduino_bytes2
            

        if "is" in arduino_bytes3:
            foundin = arduino_bytes3
            
        #Removing useless characters in the selected string 
        foundin1 = foundin.replace("b'","")
        foundin2 = foundin1[:-5]
        foundin3 = foundin2.replace(" ", "")
        foundin4 = foundin3.replace("Contentis:", "")

        #Extracting relevant information from shortened string
        Zielgeschwindigkeit = foundin4[0:3]
        Zielentfernung = foundin4[3:7]
        GKS = foundin4[7:11]

        #Removing placeholders from extracted information
        Zielgeschwindigkeit = Zielgeschwindigkeit.replace("x","")
        Zielentfernung = Zielentfernung.replace("x","")
        GKS = GKS.replace("x","")

        #Displaying extracted und processed information
        field10_label = Label(rootR, text=Zielgeschwindigkeit, font=('calibre', 10,))
        field10_label.grid(row=3, column=1)
        field20_label = Label(rootR, text=Zielentfernung, font=('calibre', 10,))
        field20_label.grid(row=4, column=1)
        field30_label = Label(rootR, text=GKS, font=('calibre', 10,))
        field30_label.grid(row=5, column=1)

    
    #Creating GUI
    rootR = Tk()

    rootR.title("BeaconCOM - Output")
    rootR.geometry("205x130")
    v = StringVar(rootR, "1")
    rootR.resizable(False, False) 
    field4_label = Label(rootR, text="Port", font=('calibre', 10,))
    field4_label.grid(row=1, column=0)
    field5_label = Label(rootR, text="", font=('calibre', 10,))
    field5_label.grid(row=2, column=0)

    field1_label = Label(rootR, text='Zielgeschwindigkeit', font=('calibre', 10,))
    field1_label.grid(row=3, column=0)

    field2_label = Label(rootR, text='Zielentfernung', font=('calibre', 10,))
    field2_label.grid(row=4, column=0)

    field3_label = Label(rootR, text='GKS(Signal)Nummer', font=('calibre', 10,))
    field3_label.grid(row=5, column=0)

    #Placeholder labels for the following values
    field100_label = Label(rootR, text="-", font=('calibre', 10,))
    field100_label.grid(row=3, column=1)
        
    field200_label = Label(rootR, text="-", font=('calibre', 10,))
    field200_label.grid(row=4, column=1)

    field300_label = Label(rootR, text="-", font=('calibre', 10,))
    field300_label.grid(row=5, column=1)

    #Creating labels just so they can be deleted right after so that the following definitions works
    field10_label = Label(rootR, text="-", font=('calibre', 10,))
    field10_label.grid(row=3, column=1)

    field20_label = Label(rootR, text="-", font=('calibre', 10,))
    field20_label.grid(row=4, column=1)

    field30_label = Label(rootR, text="-", font=('calibre', 10,))
    field30_label.grid(row=5, column=1)

    #Fetching all currently available ports and storing them in variables aswell as append them to the list "options"
    ports = serial.tools.list_ports.comports()
    port=[]
    for i in ports:
        port.append(i.device)

    numberofports = len(port)
    i=0

    options = []

    while i <= len(port) and i < numberofports:
        options.append(port[i])
        i += 1
    
    options.append(port[0])

    #Creating a dropdown-menu for port selection
    clicked = StringVar()
    clicked.set(port[1])
    drop = OptionMenu( rootR , clicked , *options )
    drop.grid(row=1, column=1)

    submit_button = Button(rootR, text ="Ablesen", command = ablesen).grid(row=7, column=1)

    rootR.mainloop()



def GUIsend():
    #Deleting previously created window for selection
    root.destroy()

    #Creating GUI
    rootS = Tk()
    rootS.title("BeaconCOM - Input")
    rootS.geometry("280x160")
    v = StringVar(rootS, "1")
    rootS.resizable(False, False) 

    field1 = StringVar()
    field2 = StringVar()
    field3 = StringVar()

    field1_label = Label(rootS, text='Zielgeschwindigkeit', font=('calibre', 10,)).grid(row=3, column=0)
    field1_entry = Entry(rootS, textvariable=field1, font=('calibre', 10, 'normal'))
    field1_entry.grid(row=3, column=1)
    field2_label = Label(rootS, text='Zielentfernung', font=('calibre', 10,)).grid(row=4, column=0)
    field2_entry = Entry(rootS, textvariable=field2, font=('calibre', 10, 'normal'))
    field2_entry.grid(row=4, column=1)
    field3_label = Label(rootS, text='GKS(Signal)Nummer', font=('calibre', 10,)).grid(row=5, column=0)
    field3_entry = Entry(rootS, textvariable=field3, font=('calibre', 10, 'normal'))
    field3_entry.grid(row=5, column=1)
    field4_label = Label(rootS, text="Port", font=('calibre', 10,))
    field4_label.grid(row=1, column=0)
    field5_label = Label(rootS, text="", font=('calibre', 10,))
    field5_label.grid(row=2, column=0)

    #Fetching all currently available ports and storing them in variables aswell as append them to the list "options"
    ports = serial.tools.list_ports.comports()
    port=[]
    for i in ports:
        port.append(i.device)

    numberofports = len(port)
    i=0

    options = []

    while i <= len(port) and i < numberofports:
        
        print(port[i])
        options.append(port[i])
        i += 1

    options.append(port[0])

    #Creating a dropdown-menu for port selection
    clicked = StringVar()
    clicked.set(port[0])

    drop = OptionMenu( rootS , clicked , *options )
    drop.grid(row=1, column=1)

    #Defining
    arduino = serial.Serial()

    #Writing to serial input
    def write_read(x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data

    #Clearing GUI entry modules after code execution
    def delete():
        field1_entry.delete(0, END)
        field2_entry.delete(0, END)
        field3_entry.delete(0, END)

    
    def submit():
        
        #Fetching port chosen by the user
        COMPORT = clicked.get()

        #Connecting to the ESP32 with DTR and RTS disabled, because it otherwise resets on establishing connection
        arduino.close()
        arduino.setDTR(False) 
        arduino.setRTS(False)
        arduino.baudrate = 115200
        arduino.port = COMPORT
        arduino.open()

        #Declaring variables for input
        ZV = field1.get()
        ZD = field2.get()
        GKS = field3.get()

        #Duplicating input variables as int for processing
        ZVint = int(ZV)
        ZDint = int(ZD)
        GKSint = int(GKS)

        #Check input values for invalid inputs 
        if(ZVint < 121 and ZDint < 1001 and GKSint < 1023 and ZVint > -1 and ZDint > -1 and GKSint > -1): 
            
            #Adding placeholders if needed to allow easier reading on the recieving side
            if(len(ZV) < 3):
                ZVLEN = 3 - len(ZV)
                if(ZVLEN == 1):
                    ZV = "".join((ZV,"x"))
                elif(ZVLEN == 2):
                    ZV = "".join((ZV,"xx"))

            if(len(ZD) < 4):
                ZDLEN = 4 - len(ZD)
                if(ZDLEN == 1):
                    ZD = "".join((ZD,"x"))
                elif(ZDLEN == 2):
                    ZD = "".join((ZD,"xx"))
                elif(ZDLEN == 3):
                    ZD = "".join((ZD,"xxx"))

            if(len(GKS) < 4):
                GKSLEN = 4 - len(GKS)
                if(GKSLEN == 1):
                    GKS = "".join((GKS,"x"))
                elif(GKSLEN == 2):
                    GKS = "".join((GKS,"xx"))
                elif(GKSLEN == 3):
                    GKS = "".join((GKS,"xxx"))
                
            #Combining all inputs after processing
            message = " ".join((ZV,ZD,GKS))

            #Writing data string to serial input
            value = write_read(message)

            #Informing the user that everything was send
            msg = Message(rootS, text = "Daten wurden übertragen!", font=('calibre', 10), width=200).grid(row=8, column=1)
            delete()
            
        else:
            #Informing the user that he gave invalid inputs
            msg = Message(rootS, text = "Eingabe ungültig!", font=('calibre', 10), width=200).grid(row=8, column=1)
            delete()

    submit_button = Button(rootS, text ="Senden", command = submit).grid(row=7, column=1)

    rootS.mainloop()

#Creation of small window for selection of the available functions
root = Tk()

root.title("BeaconCOM - Input")
root.geometry("155x50")
v = StringVar(root, "1")
root.resizable(False, False) 
field_label = Label(root, text='Funktion auswählen', font=('calibre', 10,)).grid(row=0, column=1, columnspan=2)
submit_button = Button(root, text ="Senden", command = GUIsend).grid(row=1, column=1)
submit_button = Button(root, text ="Empfangen", command = GUIreceive).grid(row=1, column=2)

root.mainloop()

#Made by Noah at BBR - 06.05.2022