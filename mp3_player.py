import tkinter as tk
from tkinter import *
from tkinter import ttk,filedialog
from tkinter.ttk import Treeview
from turtle import color
import os
from types import NoneType
import pygame
from pygame import mixer
from tinytag import TinyTag
import time

#------------------------------ Initializing window for program -------------------------
mp=Tk()
mp.iconbitmap(r'icons/rickroll.ico')
mp.title("Music Player")
mp.config(bg='#0F111A')
mp.resizable(False,False)
mp.geometry("1100x600")

#----------------------- Enter song info for playlist ---------------------------
def song_info(song,song_path):
    music=TinyTag.get(song_path)
    name=''
    if type(music.title)==NoneType:
        name=f"{song[:-4]}"
    else:
        name=music.title
    album=''
    if type(music.album)==NoneType:
        album=""
    else:
        album=music.album
    artist=''
    if type(music.artist)==NoneType:
        artist="Unknown Artist"
    else:
        artist=music.artist
    genre=''
    if type(music.genre)==NoneType:
        genre=""
    else:
        genre=music.genre
    duration=''
    if music.duration>=3600:
        duration=time.strftime('%H : %M : %S',time.gmtime(music.duration))
    else:
        duration=time.strftime('%M : %S',time.gmtime(music.duration))
    song_detail=(song_path,name,artist,album,genre,duration)
    
    return song_detail

def check_if_file(opt):
    global path
    if opt==1:
        path=filedialog.askdirectory()
        open_folder()
    else:
        path=filedialog.askopenfilename()
        j=len(path)-1
        print(path)
        print("this is length : ",j)
        song=''
        while j!=0:
            if path[j]=="/":
                song=path[j+1:]
                break
            j-=1
        rooter=[]
        for ch in path:
            if ch=='\\':
                ch='/'
            rooter.append(ch)
        rooter="".join(rooter)
        song_path=f"{rooter}"
        song_detail=song_info(song,song_path)
        if song_path in detail_list:
            pass
        else:
            with open('Playlists\Main.txt','r',encoding="utf-8") as f_read:
                elements=f_read.readlines()
                i=len(elements)
                if i%2==0:
                    playlist.insert(parent='',index=-1,iid=i,values=song_detail,tags=('even',))
                else:
                    playlist.insert(parent='',index=-1,iid=i,values=song_detail,tags=('odd',))
                i+=1
            with open('Playlists\Main.txt','a',encoding="utf-8") as f_add:
                f_add.write(f"{song_detail[0]},{song_detail[1]},{song_detail[2]},{song_detail[3]},{song_detail[4]},{song_detail[5]}\n")

#-------------- this will open a dialogue box to select song folder ------------------------------
def open_folder():
    global i,detail_list,path
    for (root,dirs,files) in os.walk(path):
        for song in files:
            if song.endswith(".mp3"):
                rooter=[]
                for ch in root:
                    if ch=='\\':
                        ch='/'
                    rooter.append(ch)
                rooter="".join(rooter)
                song_path=f"{rooter}/{song}"
                song_detail=song_info(song,song_path)
                if song_path in detail_list:
                    pass
                else:
                    with open('Playlists\Main.txt','r',encoding="utf-8") as f_read:
                        elements=f_read.readlines()
                        i=len(elements)
                        if i%2==0:
                            playlist.insert(parent='',index=-1,iid=i,values=song_detail,tags=('even',))
                        else:
                            playlist.insert(parent='',index=-1,iid=i,values=song_detail,tags=('odd',))
                        i+=1
                    with open('Playlists\Main.txt','a',encoding="utf-8") as f_add:
                        f_add.write(f"{song_detail[0]},{song_detail[1]},{song_detail[2]},{song_detail[3]},{song_detail[4]},{song_detail[5]}\n")

#------------------ Title bar, to add commands like add song -----------------------

title_bar=Label(mp,bg='black',height=2,width='400')
title_bar.pack(side=TOP)
add_folder=Button(mp,text='Add Folder',font=('',13,'bold'),fg='white',bg='#040508',bd=0,activebackground='#212942',activeforeground='#818182',command=lambda:check_if_file(1)).place(x=10,y=2)
add_file=Button(mp,text='Add File',font=('',13,'bold'),fg='white',bg='#040508',bd=0,activebackground='#212942',activeforeground='#818182',command=lambda:check_if_file(2)).place(x=120,y=2)

#------------------ Created tree to display song details -------------------------
song_frame=Frame(mp)
song_frame.place(x=0,y=27)

playlist=ttk.Treeview(song_frame,show='headings',height=19)
playlist["columns"]=('PATH','TITLE','ARTIST','ALBUM','GENRE','TIME')

#setting width of playlist columns
playlist.column('#0',width=0,stretch=NO)
playlist.column('PATH',width=0,stretch=NO)
playlist.column('TITLE',anchor=W,width=270,minwidth=50)
playlist.column('ARTIST',anchor=W,width=290,minwidth=50)
playlist.column('ALBUM',anchor=W,width=270,minwidth=50)
playlist.column('GENRE',anchor=W,width=170,minwidth=50)
playlist.column('TIME',anchor=CENTER,width=82,minwidth=50,stretch=False)

#setting headings of playlist columns     
playlist.heading('TITLE',text='TITLE',anchor=W)
playlist.heading('ARTIST',text='ARTIST',anchor=W)
playlist.heading('ALBUM',text='ALBUM',anchor=W)
playlist.heading('GENRE',text='GENRE',anchor=W)
playlist.heading('TIME',text='TIME',anchor=CENTER)

playlist["displaycolumns"]=('TITLE','ARTIST','ALBUM','GENRE','TIME')

#adding a scrollbar to the playlist
song_frame.config(height=475,width=15,bd=0)
scroll=ttk.Scrollbar(song_frame,command=playlist.yview)
playlist.config(yscrollcommand=scroll.set)
scroll.config(command=playlist.yview)
scroll.pack(side=RIGHT,fill=Y)
playlist.pack(side=LEFT)

#changing style of the playlist
style=ttk.Style()
mp.call("source","clamTheme.tcl")
style.theme_use("clam")
style.configure('Treeview',rowheight=25,fieldbackground='#252525',bd=0)
playlist.tag_configure('even',background='#2C2C2C',foreground='white')
playlist.tag_configure('odd',background='#292929',foreground='white') 


#------------------------ Adding songs saved in playlist ------------------------
i=0
file=os.getcwd()
try:
    os.mkdir(f"{file}/Playlists",0o666)
except:
    pass
f=open("Playlists/Main.txt",'a')
f.close()
detail_list=[]
with open('Playlists/Main.txt','r',encoding='utf-8') as f:
    elements=f.readlines()
    size=len(elements)
    if size==0:
        pass
    else:
        f.seek(0)
        for j in range(size):
            values=f.readline()
            values=values.split(",")
            values[5]=values[5][:-1]
            if i%2==0:
                playlist.insert(parent='',index=-1,iid=i,values=values,tags=('even',))
            else:
                playlist.insert(parent='',index=-1,iid=i,values=values,tags=('odd',))
            i+=1
            detail_list.append(values[0])
#------------------------------- Music control functions ------------------------------------

paused=True
selected=""
old_selection=""
paused=False
length=0

#............... display length of the new song ..........
def change_length(values):
    global length
    length=values[5]
    length=length.split(" : ")
    sum,i=0,len(length)-1
    while i!=-1:
        if i==len(length)-1:
            sum+=int(length[i])
        else:
            sum+=int(length[i])*60
        i-=1
    length=sum

#......... checks if music is starting or was already playing ..........

def check():
    global selected,old_selection,paused
    selected=playlist.focus()
    paused=False
    if old_selection==selected:
        resume_song()
    else:
        play_song()

#.................. resume function ......................

def resume_song():
    play.config(image=pause_button,command=pause_song)
    mixer.init()
    mixer.music.unpause()
    display_time()

#.................... play new song function ....................
def play_song():
    global selected,old_selection
    mixer.init()
    play.config(image=pause_button,command=pause_song)
    old_selection=selected
    values=playlist.item(selected,'values')
    path=values[0]
    song_name.config(text=f"{values[1]} - {values[2]}")
    change_length(values)
    mixer.music.load(path)
    slider.config(to=length,value=0)
    mixer.music.play()
    display_time()

#................... pause song .............................

def pause_song():
    global paused
    mixer.init()
    mixer.music.pause()
    paused=True
    play.config(image=play_button,command=check)
    
#..................... plays next song ............................

def next_song():
    global paused
    mixer.init()
    play.config(image=pause_button,command=pause_song)
    global selected,old_selection
    selected=str(int(selected)-1)
    playlist.focus(selected)
    playlist.selection_set(selected)
    old_selection=selected
    values=playlist.item(selected,'values')
    path=values[0]
    song_name.config(text=f"{values[1]} - {values[2]}")
    change_length(values)
    slider.config(to=length,value=0)
    if paused==False:
        play.config(image=pause_button,command=pause_song)
        mixer.music.load(path)
        mixer.music.play()
    else:
        if length>3600:
            tot_time=time.strftime('%H : %M : %S',time.gmtime(length))
        else:
            tot_time=time.strftime('%M : %S',time.gmtime(length))
        slider_timer.config(text=f"00 : 00 / {tot_time}")
        play_song()

#..................... plays previous song ......................
def previous_song():
    global paused
    mixer.init()
    play.config(image=pause_button,command=pause_song)
    global selected,old_selection
    selected=str(int(selected)+1)
    playlist.focus(selected)
    playlist.selection_set(selected)
    old_selection=selected
    values=playlist.item(selected,'values')
    path=values[0]
    song_name.config(text=f"{values[1]} - {values[2]}")
    change_length(values)
    slider.config(to=length,value=0)
    if paused==False:
        play.config(image=pause_button,command=pause_song)
        mixer.music.load(path)
        mixer.music.play()
    else:
        if length>3600:
            tot_time=time.strftime('%H : %M : %S',time.gmtime(length))
        else:
            tot_time=time.strftime('%M : %S',time.gmtime(length))
        slider_timer.config(text=f"00 : 00 / {tot_time}")
        play_song()

#............ creating a label for all commands button ......................
bottom=Label(height='10',width='1100',bg='black').place(x=0,y=540)

#----------------------------- Creating buttons -----------------------------------
previous_button=PhotoImage(file="icons/previous.png")
previous=Button(mp,image=previous_button,bd=0,bg='black',activebackground='black',command=previous_song)
previous.place(x=40,y=555.5)

play_button=PhotoImage(file="icons/play.png")
pause_button=PhotoImage(file="icons/pause.png")

play=Button(mp,image=play_button,bd=0,bg='black',activebackground='black',command=check)
play.place(x=110,y=553)

next_button=PhotoImage(file="icons/next.png")
next=Button(mp,image=next_button,bd=0,bg='black',activebackground='black',command=next_song)
next.place(x=180,y=555.5)

#------------------------- Making slider ------------------------------------
slider_timer=Label(mp,text='- / -',bg='black',fg='white')
slider_timer.place(x=760,y=541)

slider=ttk.Scale(mp,from_=0,orient=HORIZONTAL,value=0,length=600)
slider.place(x=250,y=566)

song_name=Label(mp,bg='black',fg='white')
song_name.place(x=246,y=541)
#..................... to display status time of the song ..................

def display_time():
    mixer.init()
    global length,paused,selected,old_selection
    tot_time,curr_time='',''
    current_time=mixer.music.get_pos()/1000
    if paused:
        pause_song() 
    else:
        if int(slider.get())==length:
            next_song()
        if int(slider.get())==0:
            pass
        elif int(slider.get())+1!=int(current_time):
            current_time=int(slider.get())+1
            mixer.music.play(start=current_time)

        if length>3600:
            tot_time=time.strftime('%H : %M : %S',time.gmtime(length))
            curr_time=time.strftime('%H : %M : %S',time.gmtime(current_time))
        else:
            tot_time=time.strftime('%M : %S',time.gmtime(length))
            curr_time=time.strftime('%M : %S',time.gmtime(current_time))
        
        slider_timer.config(text=f"{curr_time} / {tot_time}")
        slider.config(value=current_time)
        slider_timer.after(1000,display_time)

#--------------------- Making volume slider --------------------------------

def change_volume(x):
    mixer.init()
    mixer.music.set_volume(volume.get())
    volume_label.config(text=f"Vol : {int(mixer.music.get_volume()*100)}")
    
volume=ttk.Scale(mp,from_=0,to=1,value=1,command=change_volume)
volume.place(x=910,y=566)

volume_label=Label(mp,text=f"Vol : {int(volume.get()*100)}",bg='black',fg='white')
volume_label.place(x=905,y=541)

mp.mainloop()
