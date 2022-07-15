import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# root details
root = Tk()
root.title = "Rapid File Mover"
root.withdraw()

# function

# mover


def start_moving(target, destination):
    # target data
    target_stats = os.stat(target)
    target_filename = os.path.basename(target)
    target_sizeinmb = round(target_stats.st_size/(1024 * 1024))
    target_driveletter = os.path.splitdrive(target)[0]

    # destination data
    destination_driveletter = os.path.splitdrive(destination)[0]

    # final destination : file will be here after the program ends
    destination_final = os.path.join(destination, target_filename)

    # output

    # simple prints
    print("File Name : " + target_filename)
    print(f'File Size : {target_sizeinmb} MB')
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
        if os.path.exists(destination_final) == False:
            final_bytes = open(destination_final, "wb")
            final_bytes.write(target_bytes)
            os.remove(target)
    print("Done Copying " + target_filename)
    print("System might take some time to identify the moving process")
    print("Please Be Patient!")

# scan subfolders loop


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# program starts here


# dialog to get user choice of file
intial_folder = filedialog.askdirectory(title="Select Folder")


# checks wether user selected target or cancelled
if intial_folder:
    print("Reading Subfolders...")
    print("May take a while if the folder is so branched...")
    subfolders_list = fast_scandir(intial_folder)
    # dialog to get user choice of destination
    destination = filedialog.askdirectory(title="Select Destination")
    if destination:
        print("Starting process...")
        destination = os.path.join(
            destination, os.path.basename(intial_folder))
        if os.path.exists(destination) == False:
            os.mkdir(destination)

        for subitem_name in os.listdir(intial_folder):
            target = os.path.join(intial_folder, subitem_name)
            if os.path.isfile(target):
                start_moving(target, destination)

        for subfolder_name in subfolders_list:
            subitem_destination = subfolder_name.replace(
                intial_folder, destination)

            if os.path.exists(subitem_destination) == False:
                os.mkdir(subitem_destination)
            for subitem_name in os.listdir(subfolder_name):
                target = os.path.join(subfolder_name, subitem_name)
                if os.path.isfile(target):
                    start_moving(target, subitem_destination)

        # used to get deeper subfolders first so they are deleted before parent-folders
        subfolders_list.reverse()

        for del_sub in subfolders_list:
            try:
                os.removedirs(del_sub)
            except OSError as error:
                error = ""
        try:
            os.removedirs(intial_folder)
            print("Deleted " + intial_folder)
        except OSError as error:
            error = ""

    # confirming user input to prevent weird silent ending
    input("Press ENTER to continue.")
