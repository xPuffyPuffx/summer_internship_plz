from tkinter import *
from PIL import ImageTk,Image

#next lines concern checking, whether a character is a chinese
ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

#is char a kanji
def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

#returns kanji substrings
def cjk_substrings(string):
  i = 0
  while i<len(string):
    if is_cjk(string[i]):
      start = i
      while is_cjk(string[i]): i += 1
      yield string[start:i]
    i += 1

#string = "sdf344asfasf天地方益3権sdfsdf".decode("utf-8")
#might be useful later if i need to use decode

#reads a line from txt into 3 variables - kanji, phonetic read and english equivalent
def wholeLine(line):
    kanji = ""
    phon = ""
    word = ""
    for sub in cjk_substrings(line):
        kanji = sub
        line = line.replace(sub, "")
    phoWord = line.split(" ", maxsplit=1)
    phon = phoWord[0]
    word = phoWord[1]
    return kanji, phon, word

path1 = r'C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\HSK All Levels Vocabulary\HSK1.txt'
vBase = []
with open(path1, 'r', encoding='utf-8') as vocBase:
    for i in range(5):
        read_data = vocBase.readline()
        x, y, z = wholeLine(read_data)
        vBase.append([x, y, z])
        print("KANJI: " + x + " " + "PHON: " + y + " " + "MEANING: " + z + "\n")

root = Tk()
#---------------------------------------

topFrame = Frame(root)

#here I will put in an image
my_img = ImageTk.PhotoImage(Image.open(r"C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\pics\images (1).jfif"))
my_label = Label()#image = my_img)
my_label.grid(row=1, column = 3, rowspan = 4)

#below are all the words in english
l1 = Label(root, text = vBase[0][2])
l1.grid(row=0, sticky='S')
l2 = Label(root, text = vBase[1][2])
l2.grid(row=1, sticky='S')
l3 = Label(root, text = vBase[2][2])
l3.grid(row=2, sticky='S')
l4 = Label(root, text = vBase[3][2])
l4.grid(row=3, sticky='S')
l5 = Label(root, text = vBase[4][2])
l5.grid(row=4, sticky='S')

#below are all the entries
widthh = 15
e1 = Entry(root, width = widthh, fg = "red")
e1.grid(row=0, column = 1)
e2 = Entry(root, width = widthh, fg = "red")
e2.grid(row=1, column = 1)
e3 = Entry(root, width = widthh, fg = "red")
e3.grid(row=2, column = 1)
e4 = Entry(root, width = widthh, fg = "red")
e4.grid(row=3, column = 1)
e5 = Entry(root, width = widthh, fg = "red")
e5.grid(row=4, column = 1)

def b1conf():
  z1.set(vBase[0][1])
def b2conf():
  z2.set(vBase[1][1])
def b3conf():
  z3.set(vBase[2][1])
def b4conf():
  z4.set(vBase[3][1])
def b5conf():
  z5.set(vBase[4][1])
def confiBconf():
  if(e1.get() == vBase[0][0] and e2.get() == vBase[1][0] and e3.get() == vBase[2][0] and e4.get() == vBase[3][0] and e5.get() == vBase[4][0]):
    my_label.config(image = my_img)#grid(row=1, column = 3, rowspan = 4)

z1 = StringVar()
z1.set("")
z2 = StringVar()
z2.set("")
z3 = StringVar()
z3.set("")
z4 = StringVar()
z4.set("")
z5 = StringVar()
z5.set("")
z6 = StringVar()
z6.set("Confirm")

b1 = Button(root, textvariable = z1, width = widthh, command = b1conf)
b1.grid(row = 0, column = 2)
b2 = Button(root, textvariable = z2, width = widthh, command = b2conf)
b2.grid(row = 1, column = 2)
b3 = Button(root, textvariable = z3, width = widthh, command = b3conf)
b3.grid(row = 2, column = 2)
b4 = Button(root, textvariable = z4, width = widthh, command = b4conf)
b4.grid(row = 3, column = 2)
b5 = Button(root, textvariable = z5, width = widthh, command = b5conf)
b5.grid(row = 4, column = 2)
confiB = Button(root, textvariable = z6, width = widthh, command = confiBconf)
confiB.grid(row = 0, column = 3)

#---------------------------------------
root.mainloop()
