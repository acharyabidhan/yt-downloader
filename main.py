from tkinter import*
from pytube import YouTube
from tkinter import messagebox
from threading import Thread
import webbrowser
import os
import socket
root = Tk()
root.resizable(0,0)
window_width = 500
window_height = 220
try:root.iconbitmap("others\\icon.ico")
except:pass
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("YT Video and Audio Downloader")
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.config(background="white")
user = (os.path.split(os.path.expanduser('~'))[-1])
videoPath = f"C:\\Users\\{user}\\Videos\\"
audioPath = f"C:\\Users\\{user}\\Music\\"
a = "8.8.8.8"
b = 53
c = socket.AF_INET
d = socket.SOCK_STREAM
e = 1
global run
run = True
def checkConnection():
    while run:
        try:
            socket.setdefaulttimeout(e)
            socket.socket(c,d).connect((a,b))
            return True
        except:
            return False

def checkConnThread():
    thread = Thread(target=checkConnection)
    thread.start()
checkConnThread()
def videothread():
    thread = Thread(target=downloadVideo)
    thread.start()

def audiothread():
    thread = Thread(target=downloadaudio)
    thread.start()

def downloadBoththread():
    thread = Thread(target=downloadBoth)
    thread.start()

def downloadVideo():
    if checkConnection():
        try:
            downloadButton.config(state=DISABLED, text="Downloading")
            link = linkVar.get()
            yt = YouTube(link)
            ys = yt.streams.get_highest_resolution()
            ys.download(videoPath)
            downloadButton.config(state=NORMAL, text="Download")
            messagebox.showinfo("Download complete","Download Complete")
        except:
            messagebox.showinfo("Link","Provided link not found!!")
            downloadButton.config(text="Download", state=NORMAL)
    else:
        messagebox.showinfo("Info","No internet Connection!!")

def downloadaudio():
    if checkConnection():
        try:
            downloadButton.config(state=DISABLED, text="Downloading")
            link = linkVar.get()
            yt = YouTube(link)
            video = yt.streams.filter(only_audio=True).first()
            video.download(audioPath)
            downloadButton.config(state=NORMAL, text="Download")
            messagebox.showinfo("Download complete","Download Complete")
        except:
            messagebox.showinfo("Link","Provided link not found!!")
            downloadButton.config(text="Download", state=NORMAL)
    else:
        messagebox.showinfo("Info","No internet Connection!!")

def downloadBoth():
    if checkConnection():
        try:
            downloadButton.config(state=DISABLED, text="Downloading audio")
            link = linkVar.get()
            yt = YouTube(link)
            video = yt.streams.filter(only_audio=True).first()
            video.download(audioPath)
            downloadButton.config(state=DISABLED, text="Downloading video")
            yt = YouTube(link)
            ys = yt.streams.get_highest_resolution()
            ys.download(videoPath)
            downloadButton.config(state=NORMAL, text="Download")
            messagebox.showinfo("Download complete","Download Complete")
        except:
            downloadButton.config(text="Download", state=NORMAL)
            messagebox.showinfo("Link","Provided link not found!!")
    else:
        messagebox.showinfo("Info","No internet Connection!!")

linkVar = StringVar()
videoV = IntVar()
audioV = IntVar()

def callFunctions():
    if videoV.get() == 1 and audioV.get() == 1:
        downloadBoththread()
    elif videoV.get() == 1:
        videothread()
    elif audioV.get() == 1:
        audiothread()
    else:
        messagebox.showinfo("Options","No options selected!!")

sideFrame = Frame(root, bd=0)
sideFrame.place(x=0,y=0,width=200,height=200)

frameImg = PhotoImage(file='others\\b.png')
Label(sideFrame,image=frameImg).pack()

optionsFrame = LabelFrame(root, bd=0, bg="white", text="Options", font=("Arial",15), labelanchor="n")
optionsFrame.place(x=200,y=0,width=300,height=100)

dVideo = Checkbutton(optionsFrame,bg="white",activebackground="white",variable=videoV,font=("Arial",14),text="Download Video")
dVideo.pack()

dAudio = Checkbutton(optionsFrame,bg="white",activebackground="white",variable=audioV, font=("Arial",14),text="Download Audio")
dAudio.pack()

linkEntry = Entry(root, bd=4,textvariable=linkVar,font=("Arial",12), width=26)
linkEntry.place(relx=0.945, rely=0.670, anchor=SE)
linkEntry.insert(0,"Enter Link here!")

downloadButton = Button(root, bd=4,text="Download", activeforeground="green",font=("Arial",16),width=15, command=callFunctions)
downloadButton.place(relx=0.890, rely=0.95, anchor=SE)

def aboutmethread():
    thread = Thread(target=aboutMe)
    thread.start()

def aboutMe():
    webbrowser.open("https://www.facebook.com/bidhan.acharya.10")

menubar = Menu(root)
about = Menu(menubar, tearoff=False)
tools = Menu(menubar, tearoff=False)
menubar.add_cascade(label="About", menu=about)
menubar.add_cascade(label="Tools", menu=tools)
def nothing():
    if downloadButton["state"] == NORMAL:
        global run
        run = False
        root.destroy()
    else:
        messagebox.showinfo("Info","Downloading, Please wait!!")
tools.add_command(label="Exit", command = nothing)
about.add_command(label="About me", command=aboutmethread)
root.config(menu=menubar)
root.protocol('WM_DELETE_WINDOW', nothing)
if checkConnection() == False:
    messagebox.showinfo("Info","No internet Connection!!")
else:
    pass
root.mainloop()