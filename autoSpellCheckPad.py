from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
dictionary = ['peer','pair','allowed','aloud', 'fair','fare','peace','piece','compliment',
              'complement','brake','break','bazaar','bizarre','i','he','we',
              'they','you','who','which','what','whose','whom','where','when',
              'why','how','each','every','many','all','some','any','very','cakes'
              'much','also','his','their','your','my','delicious','cake','home','house','our','she','her','him',
              'him','them','me','us','this','that','these','those','it','its','no',
              'not','never','always','once','an','a','on','an','in','to','of','for',
              'by','with','from','very','about','mississippi','minneapolis','after','before','and','is','am','are','was',
              'were','will','shall','can','may','has','have','had','do','does','did',
              'must','should','come','go','good','be','look','read','see','name','up','right',
              'down','left','into','the','there','bakery']
dictionary = list(set(dictionary))
i=0
thisfile=None


def set_input(value):
    text.delete(1.0, "END")
    text.insert("end-1c", value)


def get_words():
    words = text.get("1.0",END).split()
    print(words)


def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],
                                   dp[i-1][j],
                                   dp[i-1][j-1])
    return dp[m][n]

def Autocorrect(word):
    dists =  []
    for i in range(len(dictionary)):
        dists.append(editDistDP(word, dictionary[i], len(word), len(dictionary[i])))
    arr2 = sorted(dists)
    min_dist = arr2[0]
    for i in range(len(dists)):
        if min_dist == dists[i]:
            minpos=i
            break
    return dictionary[minpos]

def autocorrect():
    words = text.get("1.0",END).split()
    in_word = words[-1]
    
    out =Autocorrect(in_word)
    label.config(text = out)

def correctWord(event):
    words = text.get("1.0",END).split()
    if len(words)!=0:
        text.delete('1.0', END)
        for i in range(len(words)-1):
            text.insert("end-1c", words[i])
            text.insert("end-1c", " ")
        text.insert("end-1c", label.cget("text")+" ")

def checkSpelling(event):
    autocorrect()

def newLine(event):
    autocorrect()

def saveFile():
    global i
    if i==0:
        file = filedialog.asksaveasfile(initialdir="D:\\Main",
                                        defaultextension='.txt',
                                        filetypes=[
                                            ("Text file",".txt"),
                                            ("HTML file", ".html"),
                                            ("All files", ".*"),
                                        ])
        if file is None:
            return
        else:
            global thisfile
            thisfile = file
        filetext = str(text.get(1.0,END))
        file.write(filetext)
        i = i + 1
    else:
        currentFileSave()

def currentFileSave():
    global thisfile
    thisfile.truncate(0)
    filetext = str(text.get(1.0,END))
    thisfile.write(filetext)
    thisfile.close()



window = Tk()
window.title("AutoSpellCheckPad")
def on_closing():
    if messagebox.askyesno("Quit", "Do you want to exit?"):
        global thisfile
        try:
            thisfile.close()
        except:
            pass
        window.destroy()

def aboutUs():
    messagebox.showinfo(title="About Us",message="This application is for writing text files without spell errors.")

def manual():
    messagebox.showinfo(title="User Tips",message="->Avoid writing in the middle of words, type sequentially.\n->Save the file after editing.\n->To change the current word into suggested word, click the 'insert' button.")
window.protocol("WM_DELETE_WINDOW", on_closing)


menubar = Menu(window)
window.config(menu=menubar)

fileMenu = Menu(menubar,tearoff=0,font=("Consolas",10))

aboutMenu = Menu(menubar,tearoff=0,font=("Consolas",10))
menubar.add_cascade(label="About",menu=aboutMenu)
aboutMenu.add_command(label="User Manual",command=manual,image=None,compound='left')
aboutMenu.add_command(label="About us",command=aboutUs,image=None,compound='left')
label2 = Label(window,
              text="Do you mean",
              font=('Arial',20,'bold'),
              fg='#00FF00',
              bg='black',
              relief=RAISED,
              bd=5,
              padx=5,
              pady=5,
              compound='bottom')
label2.pack()
label = Label(window,
              text="this word",
              font=('Arial',30,'bold'),
              fg='#00FF00',
              bg='black',
              relief=RAISED,
              bd=10,
              padx=10,
              pady=10,
              compound='bottom')
label.pack()
#label.place(x=0,y=0)
text = scrolledtext.ScrolledText(window,
            bg="light yellow",
            font=("Consolas",25),
            height=10,
            width=30,
            padx=20,
            pady=20,
            fg="purple",
            wrap=WORD)
text.pack()
button = Button(text='save',command=saveFile)
button.pack()
window.bind('<KeyRelease>',checkSpelling)
window.bind("<Return>",newLine)
window.bind('<Insert>',correctWord)
window.mainloop()



