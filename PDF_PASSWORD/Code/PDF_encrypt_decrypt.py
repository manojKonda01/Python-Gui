import PyPDF2
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil

win = Tk()
win.geometry("220x380")
win.title("PDF Encryption and Decryption")
# PNG
p1 = PhotoImage(file="images/img1.png").subsample(10)
p2 = PhotoImage(file="images/down.png").subsample(15)
p3 = PhotoImage(file="images/browse.png").subsample(2)
p4 = PhotoImage(file="images/encrypt.png").subsample(2)
p5 = PhotoImage(file="images/decrypt.png").subsample(2)
p6 = PhotoImage(file="images/uploaded.png").subsample(2)

# Title image
imglabel = Label(image=p1)
imglabel.grid(row=0, columnspan=5)

help = Label(win, text="Enter password")
help.grid(columnspan=5, row=4)

# Password
passwd = Entry(win, text="Enter Password", show="*", width=30)
passwd.grid(row=5, columnspan=5)

ongoing = ""


# Browse
def browse():
    global filename
    filename = filedialog.askopenfile(mode='rb', title="Choose a Pdf file",
                                      filetypes=[("PDF", "*.pdf*")])
    select.configure(image=p6)


# PDF locker
def encrypt():
    global ongoing
    ongoing = "encrypt"
    global name
    assert isinstance(filename, object)
    name = (str(filename).split('/')[-1]).split('.pdf')[0]
    if filename is not None:
        fil = PyPDF2.PdfFileReader(filename)
        out = PyPDF2.PdfFileWriter()
        for i in range(fil.numPages):
            out.addPage(fil.getPage(i))
        if passwd.get():
            out.encrypt(passwd.get())
            with open(name + "_encrypted.pdf", 'wb') as filee:
                out.write(filee)
            filee.close()
            passwd.delete(0, "end")
            messagebox.showinfo("Success", "File encrypted Successfully")
            messagebox.showwarning("Remember Password", "If you forget Password Encrypt again")
            pathlabel.configure(text="Click hereto Download the Encrypted PDF file", fg="blue")
            select.configure(image=p3)
            win.geometry("260x380")
        else:
            messagebox.showerror("Invalid Password", "Password should not be NULL")

    else:
        messagebox.showerror("Failed", "Unable to encrypt file")


# PDF delocker
def decrypt():
    global ongoing
    ongoing = "decrypt"
    global nam
    assert isinstance(filename, object)
    nam = (str(filename).split('/')[-1]).split('.pdf')[0]
    if filename is not None:
        fil = PyPDF2.PdfFileReader(filename)
        out = PyPDF2.PdfFileWriter()
        if fil.isEncrypted:
            if not passwd.get():
                messagebox.showinfo("Invalid Password", "Password should not be NULL")
            elif passwd.get():
                fil.decrypt(passwd.get())
                for i in range(fil.numPages):
                    out.addPage(fil.getPage(i))
                with open(nam + "_decrypted.pdf", 'wb') as filee:
                    out.write(filee)
                filee.close()
                passwd.delete(0, "end")
                messagebox.showinfo("Success", "File Decrypted Successfully")
                pathlabel.configure(text="CLick here to Download the Decrypted PDF file", fg="blue")
                select.configure(image=p3)
                win.geometry("260x380")
        else:
            messagebox.showinfo("Decrypted file", "File already decrypted")
    else:
        messagebox.showerror("Failed", "Unable to Decrypt file")


# download
def download():
    if ongoing == 'encrypt':
        try:
            shutil.move(name + "_encrypted.pdf", filedialog.askdirectory())
            messagebox.showinfo("Downloaded", "Downloaded Successfully")
        except NameError:
            messagebox.showinfo("Choose File", "Choose to encrypt")
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "Encrypt/decrypt first")
        except shutil.SameFileError:
            messagebox.showinfo("Same File Error", "Download somewhere else")
    elif ongoing == 'decrypt':
        try:
            shutil.move(nam + "_decrypted.pdf", filedialog.askdirectory())
            messagebox.showinfo("Downloaded", "Downloaded Successfully")
        except NameError:
            messagebox.showinfo("Choose File", "Choose to decrypt ")
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "Encrypt/decrypt first")
        except shutil.SameFileError:
            messagebox.showinfo("Same File Error", "Download somewhere else")
    else:
        messagebox.showinfo("Browse", "Upload PDF file ")


pathlabel = Label(win, text="Encrypt/Decrypt here", fg="blue")
select = Button(win, image=p3, command=browse)
en = Button(win, image=p4, command=encrypt).grid(row=6, column=2)
de = Button(win, image=p5, command=decrypt).grid(row=6, column=3)
ben = Button(win, image=p2, command=download).grid(row=9, columnspan=5)
exi = Button(win, text="Exit", command=exit).grid(row=10, columnspan=5)
Label(win).grid(row=5)
Label(win).grid(row=3)
pathlabel.grid(row=7, columnspan=5)
select.grid(row=1, columnspan=5)
win.mainloop()
