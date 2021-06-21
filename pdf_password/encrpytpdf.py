import PyPDF2
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
win = Tk()
win.geometry("500x500")
win.title("PDF Encryption")
p1 = PhotoImage(file="img1.png")
p1 = p1.subsample(10)
imglabel = Label(image=p1)
imglabel.image = p1
imglabel.grid(rows=1,column=1)
help = Label(win,text="Enter password and choose file ")
help.grid(columnspan=4,rows=2)
passwd = Entry(win, text="Enter Password", show="*", width=15)
passwd.grid(rows=3, column=1)
def browse():
    filename = filedialog.askopenfile(mode='rb', title="Choose a Pdf file", filetypes=(("PDF", "*.pdf"), ("all Files", "*.*")))
    name = (str(filename).split('/')[-1]).split('.pdf')[0]
    if filename is not None:
        fil = PyPDF2.PdfFileReader(filename)
        out = PyPDF2.PdfFileWriter()
        for i in range(fil.numPages):
            out.addPage(fil.getPage(i))
        if passwd.get():
            out.encrypt(passwd.get())
            with open(name+"_encrypted.pdf", 'wb') as filee:
                out.write(filee)
            filee.close()
            passwd.delete(0,"end")
            messagebox.showinfo("Success", "File encrypted Successfully")
            messagebox.showwarning("Remember Password","If you forget Password Encrypt again")
        else:
            messagebox.showerror("Invalid Password", "Enter password")

    else:
        messagebox.showerror("Failed", "Unable to encrypt file")


win.config(background="white")
brows = Button(win, text="Browse File", command=browse)
exi = Button(win, text="Exit", command=exit)
#pathlabel.grid(rows=1, column=1)
brows.grid(rows=1, column=1)
exi.grid(rows=2, column=1)
win.mainloop()


