from tkinter import *
from os import listdir, path, walk
import shutil
from send2trash import send2trash
import tkinter.font as font

# ------------------------------functions------------------------------


def check():
    T1.delete("1.0", END)
    T1.insert(END, f"{E1.get()}\n")
    T1.insert(END, f"{len(listdir(E1.get()))} files\n")
    T1.insert(END, listdir(E1.get())[0:10])


def delete():
    filename = path.join(E1.get(), listdir(E1.get())[0])
    filename2 = path.join(E1.get(), f"full{listdir(E1.get())[0]}")
    send2trash(filename)
    # below function is specific to news_classification data
    if path.isfile(filename2) == True:
        send2trash(filename2)
    else:
        print("no file with that name", filename2)


def get_text():
    # delete previous text. Dont know what END stands for
    T1.delete("1.0", END)
    filename = path.join(E1.get(), listdir(E1.get())[0])
    with open(filename, 'r') as f:
        T1.insert(INSERT, f.read())


def move_text(directory_destination):
    filename = listdir(E1.get())[0]
    source = path.join(E1.get(), filename)
    destination = path.join(directory_destination, filename)
    shutil.move(source, destination)
    # below function is specific to news_classification data
    filename2 = f"full{filename}"
    source2 = path.join(E1.get(), filename2)
    if path.isfile(source2) == True:
        destination2 = path.join(
            r"E:\Study\FastAI\Text Classifier\reference text", filename2)
        shutil.move(source2, destination2)
    else:
        print("no file with that name", source2)


def when_deleting():
    delete()
    get_text()


def when_moving(directory_destination):
    move_text(directory_destination)
    get_text()

# ------------------------------Structure--------------------------------


root = Tk()
root.geometry("600x600")
root.minsize(width=600, height=600)
root.maxsize(width=1920, height=1080)
root.title(f"Categorizer")

main_frame = Frame(root, bg="white")
main_frame.pack(side=TOP, fill=BOTH, expand=1)

# Create options frame for setting the directory of the source folder.
option1 = Frame(main_frame, bg="gray")
option1.pack(side=TOP, fill=X)

L1 = Label(option1, text="Input(Source) Folder", font=(
    "", 13)).pack(side=LEFT, anchor=NW)
E1 = Entry(option1, font=('', 13),  borderwidth=2, relief="sunken")
E1.insert(END, r"E:\Study\FastAI\Text Classifier\to_classify")
E1.pack(side=LEFT, anchor=NW, fill=X, expand=1)
B1 = Button(option1, text="Start", command=get_text).pack(side=LEFT, anchor=NE)

T1 = Text(main_frame, wrap=WORD, borderwidth=10,
          relief="sunken", font=("Ubuntu", 12))
T1.insert(END, E1.get())
T1.pack(side=TOP, anchor=NW, fill=BOTH, expand=1)

# Create the buttons and rest
positive_directory = r"E:\Study\FastAI\Text Classifier\pos"
negative_directory = r"E:\Study\FastAI\Text Classifier\neg"

L2 = Label(main_frame, text=f"Positive Output Locations:    {positive_directory}").pack(
    side=TOP, anchor=NW)
L3 = Label(main_frame, text=f"Negative Output Locations:    {negative_directory}").pack(
    side=TOP, anchor=NW)
option2 = Frame(main_frame, bg="yellow")
option2.pack(side=TOP, fill=X)

helv28 = font.Font(family='Helvetica', size=28, weight='bold')

B2 = Button(option2, text="positive", command=lambda: when_moving(
    positive_directory), bg="green", font=helv28).pack(side=LEFT, expand=1, fill=X)
B3 = Button(option2, text="Delete", command=when_deleting,
            bg="gray", font=helv28).pack(side=LEFT, expand=1, fill=X)
B4 = Button(option2, text="Negative", command=lambda: when_moving(
    negative_directory), bg="red", font=helv28).pack(side=LEFT, expand=1, fill=X)

root.mainloop()
