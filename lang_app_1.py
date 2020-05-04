from tkinter import *
from PIL import ImageTk,Image
import random
import time
import datetime
from operator import itemgetter
import os, random

#here i arbitrarily set minimum time intervals that have to pass beofre a word at a particular
#level can be checked
minuteIntervals = [1,4,16,64,256,2048,8192,32768]
class wordling():
  def __init__(self, x, y, z, score = 0, date = datetime.datetime.now(), totalTime = 0, isUsed = 0):
    self.x = x
    self.y = y
    self.z = z
    self.score = score
    self.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    self.totalTime = totalTime
    self.isUsed = isUsed
  def __reScore__(self, guessed, usedHelp, timeStamp = datetime.datetime.now()):
    #self.date = timeStamp - weź to wywal jak będziesz trzeźwy
    self.isUsed = 0
    if(self.date == None):
      self.date = timeStamp
    else:
      timediff = timeStamp - self.date
      self.totalTime = int(self.totalTime) + timediff.seconds
      self.date = timeStamp
    #self.totalTime = ...
    if(guessed == 1 and usedHelp == 0):
      self.score = int(self.score) + 1
    else:
      self.score = int(self.score) - 1
    if(self.score == 0 or self.score == -1):
      self.score = 1
      self.totalTime = 0
  def __actualize__(self): #here we will occasionally change category to 1 from 0, or to 7 from 8
    pass
  def __getitem__(self, key):
    if(key == 0):
      return self.x
    elif(key == 1):
      return self.y
    elif(key == 2):
      return self.z
    elif(key == 3):
      return self.score
    elif(key == 4):
      return self.date
    elif(key == 5):
      return self.totalTime
    elif(key == 6):
      return self.isUsed
  def __setitem__(self, key, value):
    if(key == 0):
      self.x = value
    elif(key == 1):
      self.y = value
    elif(key == 2):
      self.z = value
    elif(key == 3):
      self.score = value
    elif(key == 4):
      self.date = value
    elif(key == 5):
      self.totalTime = value
    elif(key == 6):
      self.isUsed = value

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
    #for sub in cjk_substrings(line):
    #    kanji = sub
    #    line = line.replace(sub, "")[:-1]
    phoWord = line.split("!!!")
    phon = phoWord[0]
    word = phoWord[1]
    return phoWord[0], phoWord[1], phoWord[2], phoWord[3], phoWord[4], phoWord[5]

path1 = r'C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\HSK All Levels Vocabulary\HSK1.txt'
path2 = r'C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\vocPriv\Prof1.txt'
path3 = r'C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\vocPriv\Prof2.txt'

#function for saving changes in profile text file
def onClosing(vBase, entries, toUse, usedHelp, root):
  vBase = vBase
  entries = entries
  toUse = toUse
  usedHelp = usedHelp
  root = root
  with open(path2, 'w', encoding='utf-8') as f:
    for i in range(5):
      index = vBase.index(toUse[i])
      if(entries[i].get() == toUse[i][0]):
        guessed = 1
      else:
        guessed = 0
      vBase[index].__reScore__(guessed, usedHelp[i])
    for i in vBase:
      f.write("!!!".join([str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6])]) + "\n")
  root.destroy()


def loopKtoK():
  vBase = []
  #here I will need to change this function, so that words to check would be chosen
  #based on their score
  with open(path2, 'r', encoding='utf-8') as vocBase:
    vocLines = vocBase.readlines()
    for i in vocLines:
        read_data = i
        #x, y, z = wholeLine(read_data)
        #vBase.append([x,y,z])
        vBase.append(wordling(*wholeLine(read_data)))
  root = Tk()
  #---------------------------------------
  #here we sort vBase based on scores, ignoreing words that are already being used somewhere
  sorted(vBase, key=itemgetter(6,3))
  topFrame = Frame(root)
  #here I will put in an image
  rawDir = r"C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\pics\ "
  picAddress = rawDir[:-1]  +  random.choice(os.listdir(r"C:\Users\KompPiotra\Desktop\Nauka - Jakub\projekt_cn\pics"))
  my_img = ImageTk.PhotoImage(Image.open(picAddress))
  my_label = Label()#image = my_img)
  my_label.grid(row=1, column = 3, rowspan = 4)

  #variable recording instances of pressing buttons with help
  usedHelp = [0,0,0,0,0]

  #variable storing wordlings to be used, we will need to it get their indices at the end
  toUse = []
  for i in vBase:
    if(len(toUse)>4): break
    timeSinceCheck = datetime.datetime.now() - i.date
    if(i[6]==0 and timeSinceCheck.seconds/60 >= minuteIntervals[int(i[3])]):
      toUse.append(i)

  #below are all the words in english
  l1 = Label(root, text = toUse[0][2])
  l1.grid(row=0, sticky='S')
  l2 = Label(root, text = toUse[1][2])
  l2.grid(row=1, sticky='S')
  l3 = Label(root, text = toUse[2][2])
  l3.grid(row=2, sticky='S')
  l4 = Label(root, text = toUse[3][2])
  l4.grid(row=3, sticky='S')
  l5 = Label(root, text = toUse[4][2])
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
  entries = [e1,e2,e3,e4,e5]

  def b1conf():
    z1.set(toUse[0][1])
    usedHelp[0] = 1
  def b2conf():
    z2.set(toUse[1][1])
    usedHelp[1] = 1
  def b3conf():
    z3.set(toUse[2][1])
    usedHelp[2] = 1
  def b4conf():
    z4.set(toUse[3][1])
    usedHelp[3] = 1
  def b5conf():
    z5.set(toUse[4][1])
    usedHelp[4] = 1
  def confiBconf():
    if(e1.get() == toUse[0][0] and e2.get() == toUse[1][0] and e3.get() == toUse[2][0] and e4.get() == toUse[3][0] and e5.get() == toUse[4][0]):
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
  exitB = Button(root, text = "Exit", width = widthh, command = lambda:onClosing(vBase, entries, toUse, usedHelp, root))
  exitB.grid(row = 5, column = 2)
  #---------------------------------------
  root.protocol("WM_DELETE_WINDOW", onClosing)
  root.mainloop()
  time.sleep(3)
for i in range(2):
  loopKtoK()