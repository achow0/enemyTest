import math
import tkinter as tk
from pynput import keyboard

#pynput functions
def key_to_str(key):
    numpadDict={f"{i+96}": str(i) for i in range(10)}
    numpadDict["110"]="."
    ctrlDict={f"'\\x0{i}'": chr(i+96) for i in range(1,9)}
    tmpDict={"'\\t'":"i",
             "'\\n'":"j",
             "'\\x0b'":"k",
             "'\\x0c'":"l",
             "'\\r'":"m",
             "'\\x0e'":"n",
             "'\\x0f'":"o",
             "'\\x1a'":"z",
             "'\\x1b'":"[",
             "'\\x1c'":"\\",
             "'\\x1d'":"]",
             "'\\x1e'":"^",
             "'\\x1f'":"_",
             "'\\x00'":"2",
             "'\\\\'":"\\"}
    tmpDict.update({f"'\\x{i}'": chr(i+102) for i in range(10,20)})
    ctrlDict.update(tmpDict)
    if str(key)==None:
        strkey=str(key.vk)
    elif str(key)[0]=="<" and str(key)[-1]==">":
         strkey=numpadDict[str(key.vk)]
    elif "Key." in str(key):
        strkey=key.name
    elif "'" in str(key):
        if "\\" in str(key):
            strkey=ctrlDict[str(key)]
        else:
            strkey=str(key.char)
    else:
        strkey=str(key)
    return strkey

def on_press(key):
    global keypress_list
    key=key_to_str(key)
    if not key in keypress_list:
        keypress_list.append(key)

    
def on_release(key):
    global keypress_list
    key=key_to_str(key)
    keypress_list.remove(key)

#check last phase
def last_phase(last,n):
    phase_list=[f"{i} Phase" for i in ["Orbit", "Rush", "Run"]]
    if last!=n:
        print(phase_list[n])
    return n

#check if player or gunner is going to move out of bounds
def within_border_check(n, length):
    max_bound=800-length
    return n if length<=n<=max_bound else [length,max_bound][n>max_bound]
    
#gunner movement
def gunner_check(lastPhase=-1):
    global r, center_x, center_y, gunner_x, gunner_y, gunner, gunner_speed, gunner_length, millisecondRate
    PI=math.pi
    dx=center_x-gunner_x
    dy=center_y-gunner_y
    g_to_p_ang=math.atan2(dy,dx)
    p_to_g_ang=PI+g_to_p_ang
    dist=math.sqrt(dx*dx+dy*dy)
    ang_increase=gunner_speed/r
    t=p_to_g_ang
    if abs(dist-r)<=gunner_speed:#basically on the orbit
        lastPhase=last_phase(lastPhase,0)
        t+=ang_increase
        gunner_x=r*math.cos(t)+center_x
        gunner_y=r*math.sin(t)+center_y
    elif dist>r:#far from orbit
        lastPhase=last_phase(lastPhase,1)
        gunner_x+=gunner_speed*math.cos(g_to_p_ang)
        gunner_y+=gunner_speed*math.sin(g_to_p_ang)
    elif dist<r:#far inside of orbit
        lastPhase=last_phase(lastPhase,2)
        gunner_x+=gunner_speed*math.cos(p_to_g_ang)
        gunner_y+=gunner_speed*math.sin(p_to_g_ang)
    gunner_x=within_border_check(gunner_x, gunner_length)
    gunner_y=within_border_check(gunner_y, gunner_length)
    canvas.coords(gunner, gunner_x-gunner_length, gunner_y-gunner_length, gunner_x+gunner_length, gunner_y+gunner_length)
    root.after(millisecondRate, gunner_check, lastPhase)

#player movement
def movement():
    global keypress_list, speed, center_x, center_y, speed, safe_circle, r, player, player_length, millisecondRate
    dx=0
    dy=0
    if "down" in keypress_list:
        dy+=speed
    if "up" in keypress_list:
        dy-=speed
    if "left" in keypress_list:
        dx-=speed
    if "right" in keypress_list:
        dx+=speed
    center_x+=dx
    center_y+=dy
    center_x=within_border_check(center_x, player_length)
    center_y=within_border_check(center_y, player_length)
    canvas.coords(safe_circle, center_x-r, center_y-r, center_x+r, center_y+r)
    canvas.coords(player, center_x-player_length, center_y-player_length, center_x+player_length, center_y+player_length)
    root.after(millisecondRate, movement)

#tkinter canvas
root=tk.Tk()
canvas=tk.Canvas(root, height=800, width=800)
root.resizable(False, False)
root.title("Enemy Movement Test")

#player stats
center_x=400#player start pos x-coord
center_y=400#player start pos y-coord
speed=10#player's speed
player_length=20#player's length/width
player_length/=2

#gunner stats
gunner_x=10#gunner start pos x-coord
gunner_y=10#gunner start pos y-coord
gunner_speed=5#gunner's speed
gunner_length=20#gunner's length/width
r=100#safe distance
gunner_length/=2

#framerate
updateRate=10#update this many times per second
millisecondRate=1000//updateRate

#creating widgets
player=canvas.create_rectangle(center_x-player_length, center_y-player_length, center_x+player_length, center_y+player_length)
gunner=canvas.create_rectangle(gunner_x-gunner_length, gunner_y-gunner_length, gunner_x+gunner_length, gunner_y+gunner_length)
safe_circle=canvas.create_oval(center_x-r, center_y-r, center_x+r, center_y+r)

#keyboard input setup
keypress_list=[]
listener=keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

#initialize main logic
canvas.pack()
root.after(millisecondRate,gunner_check)
root.after(millisecondRate, movement)
root.mainloop()
