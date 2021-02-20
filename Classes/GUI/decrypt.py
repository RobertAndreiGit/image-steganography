import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

from Classes.steganography import doDecoding


def do_decrypt():
    print("do_encrypt")

def choose_image():
    filename = askopenfilename(filetypes=[("Image File",'.png')])
    pathLabel['text']=filename

def choose_path():
    folderpath = askdirectory()
    folderPath['text'] = folderpath

def decode():
    try:
        if e1.get() != '' and e2.get() != '' and folderPath['text']!='' and pathLabel['text']!='':
            doDecoding(pathLabel['text'], e1.get(), e2.get(), folderPath['text'])
            tk.messagebox.showinfo(title="DONE", message="Decryption Done")
        else:
            tk.messagebox.showerror(title="FAIL", message="Make sure you added all parameters")
    except:
        tk.messagebox.showerror(title="ERROR", message="Make sure you provided the correct information")

def createWindow():
    global e1, e2, folderPath, pathLabel

    root = tk.Tk()
    root.title("Image Steganography - Decrypt")
    root.geometry("600x100")
    root.resizable(0,0)
    menu = tk.Menu(root)
    root.config(menu=menu)

    tk.Label(root, text="Encryption Password").grid(row=0)
    tk.Label(root, text="Key").grid(row=1)
    pathLabel = tk.Label(root, text='')
    pathLabel.grid(row=2, column=1)
    folderPath = tk.Label(root, text='')
    folderPath.grid(row=3, column=1)

    e1 = tk.Entry(root)
    e2 = tk.Entry(root)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    button = tk.Button(root,
                       text="Choose Encrypted Image",
                       command=choose_image)
    button.grid(row=2, column=0)
    button = tk.Button(root,
                       text="Choose Output Folder",
                       command=choose_path)
    button.grid(row=3, column=0)
    button = tk.Button(root,
                       text="Decrypt",
                       command=decode)
    button.grid(row=4, column=1)

    root.mainloop()