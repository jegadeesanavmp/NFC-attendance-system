import streamlit as st 
import serial
import csv
from datetime import datetime
import putGit
import time 
import threading

st.write("Place the card")
ser = None  # Initialize serial port as None

def open_serial_port():
    global ser
    try:
        ser = serial.Serial('COM6', 9600)  # Change 'COM6' to the correct serial port
    except serial.SerialException as e:
        st.error(f"Failed to open serial port: {e}")
        return False
    return True

def close_serial_port():
    global ser
    if ser:
        ser.close()

def check():
    if not open_serial_port():
        return
    
    l = []
    d={"f3f6d7fa":"Mithun 23CSEA47","c3066bdd":"jegadeeshh  23CSEA45"}
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().strip().decode() 
            uid_index = data.find("UID:")
            if uid_index != -1:
                uid_value = data[uid_index + 5:uid_index + 13]
                uid = uid_value.split()
                if len(uid[0]) > 2 and uid[0] not in l:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    if {'Name': d.get(uid[0], 'Unknown'), 'UID': uid[0], 'Check-in Time': current_time} not in l:
                        l.append({'Name': d.get(uid[0], 'Unknown'), 'UID': uid[0], 'Check-in Time': current_time})
                        st.write("Detected!")
                    with open('check_in_data.csv', mode='w', newline='') as file:
                        fieldnames = ['Name', 'UID', 'Check-in Time']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        for entry in l:
                            writer.writerow(entry)
                    
                    

def update():
    check_count = 0
    while True:
        time.sleep(1)
        check_count += 1
        if check_count == 60:
            putGit.updateGit()
            check_count = 0
            print("Updated")

thread1 = threading.Thread(target=check)
thread2 = threading.Thread(target=update)

thread1.start()
thread2.start()

