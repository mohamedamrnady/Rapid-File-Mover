import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from typing import final

# root details
root = Tk()
root.title = "Rapid File Mover"
root.withdraw()

# dialog to get user choice of file
target_list = filedialog.askopenfilenames(title="Select File")


# checks wether user selected target or cancelled
if target_list:

    # dialog to get user choice of destination
    destination = filedialog.askdirectory(title="Select Destination")
    if destination:
        for target in target_list:
            # target data
            target_stats = os.stat(target)
            target_filename = os.path.basename(target)
            target_sizeinmb = round(target_stats.st_size/(1024 * 1024))
            target_driveletter = os.path.splitdrive(target)[0]

            # destination data
            destination_driveletter = os.path.splitdrive(destination)[0]

            # final destination : file will be here after the program ends
            destination_final = destination + "/" + target_filename

            # output

            # simple prints
            print("File Name : " + target_filename)
            print(f'File Size : {target_sizeinmb} MB')
            print("Destination : " + destination)
            print("Operation Started")

            # checks wether file on same drive or NOT
            if target_driveletter == destination_driveletter:
                os.rename(target, destination_final)
                print("Done Copying " + target_filename)
            if not target_driveletter == destination_driveletter:
                target_bytes = open(target, "rb").read()
                if os.path.exists(destination_final) == True:
                    msg = messagebox.askokcancel(
                        "Error", "File Already Found in Destination, Replace?")
                    if msg == True:
                        # delete exsiting file with the same name
                        os.remove(destination_final)
                        final_bytes = open(destination_final, "wb")
                        final_bytes.write(target_bytes)
                        os.remove(target)
                        final_bytes.close()
                if os.path.exists(destination_final) == False:
                    final_bytes = open(destination_final, "wb")
                    final_bytes.write(target_bytes)
                    os.remove(target)
                    final_bytes.close()
            print("Done Copying " + target_filename)
        # confirming user input to prevent weird silent ending
        input("Press ENTER to continue.")
