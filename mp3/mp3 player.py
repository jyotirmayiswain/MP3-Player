from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('MP3 player')
root.iconbitmap('ipod_mini_pink.ico')
root.geometry("500x450")

#initialize the pygame mixer
pygame.mixer.init()

#grab some length time info
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    #convert to time format
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
    
    
    song = song_box.get(ACTIVE)
    song = f'C:/Users/hp/Downloads/{song}.mp3'
    
    #get song length from mutagen
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))

    status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length}  ')
    my_slider.config(value=current_time)
    status_bar.after(1000, play_time)

#add song
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song = song.replace("C:/Users/hp/Downloads/","")
    song = song.replace(".mp3","")
    song_box.insert(END,song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    
    for song in songs:
        song = song.replace("C:/Users/hp/Downloads/","")
        song = song.replace(".mp3","")
        song_box.insert(END,song)

def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/hp/Downloads/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #call play time func
    play_time()
    #update slider position
    slider_position = int(song_length)
    my_slider.config(to=slider_position,value=0)

def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #clear status bar
    status_bar.config(text='')

def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/hp/Downloads/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear active bar in playlist 
    song_box.selection_clear(0,END)
    #activate next song
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = f'C:/Users/hp/Downloads/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear active bar in playlist 
    song_box.selection_clear(0,END)
    #activate next song
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
 
def delete_all_songs():
    song_box.delete(0,END)
    pygame.mixer.music.stop()

#create global pause
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True 

def slide(x):
    slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')


   
    
#create playlist
song_box = Listbox(root,bg="black",fg="orange",width=60,selectbackground="gray",selectforeground="black")
song_box.pack(pady=20)


# player control button
back_btn=PhotoImage(file='rewind.png')
forward_btn=PhotoImage(file='forward.png')
play_btn=PhotoImage(file='play.png')
pause_btn=PhotoImage(file='pause.png')
stop_btn=PhotoImage(file='stop.png')

#create player buttons
control_frame= Frame(root)
control_frame.pack()

back_button=Button(control_frame,image=back_btn,borderwidth=0,command=previous_song)
forward_button=Button(control_frame,image=forward_btn,borderwidth=0,command=next_song)
play_button=Button(control_frame,image=play_btn,borderwidth=0,command=play)
pause_button=Button(control_frame,image=pause_btn,borderwidth=0,command=lambda: pause(paused))
stop_button=Button(control_frame,image=stop_btn,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=1,padx=10)
forward_button.grid(row=0,column=4,padx=10)


#create menu
my_menu=Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Add songs",menu=add_song_menu)
add_song_menu.add_command(label="Add song to playlist",command=add_song)
#add many songs
add_song_menu.add_command(label="Add Many Songs to Playlist",command=add_many_songs)

#delet song
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu= remove_song_menu)
remove_song_menu.add_command(label="Delerte a song from playlist",command=delete_song)
remove_song_menu.add_command(label="Delerte a songs from playlist",command=delete_all_songs)

#status bar
status_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#slider
my_slider = ttk.Scale(root,from_
= 0, to=100, orient = HORIZONTAL,value = 0,command=slide,length=360)
my_slider.pack(pady=30)
 
#create label
slider_label = Label(root,text="0")
slider_label.pack(pady=10)

root.mainloop()