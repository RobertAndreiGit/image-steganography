import tkinter as tk
from Classes.GUI.encrypt import createWindow as showEncrypt
from Classes.GUI.decrypt import createWindow as showDecrypt

def open_encrypt():
    showEncrypt()

def open_decrypt():
    showDecrypt()

root = tk.Tk()
root.title("Image Steganography")
root.geometry("300x100")
root.resizable(0,0)
frame = tk.Frame(root)
frame.pack()
menu = tk.Menu(root)
root.config(menu=menu)

button = tk.Button(frame,
                   text="Encrypt",
                   command=open_encrypt)
button.pack(side=tk.LEFT)
slogan = tk.Button(frame,
                   text="Decrypt",
                   command=open_decrypt)
slogan.pack(side=tk.LEFT)

root.mainloop()