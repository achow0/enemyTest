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

#gunner movement
def gunner_check():
    global r, center_x, center_y, gunner_x, gunner_y, gunner, gunner_speed
    PI=math.pi
    dx=center_x-gunner_x
    dy=center_y-gunner_y
    ndx=-dx
    ndy=-dy
    g_to_p_ang=math.atan2(dy,dx)
    p_to_g_ang=math.atan2(ndy,ndx)
    dist=math.sqrt(dx*dx+dy*dy)
    ang_increase=(gunner_speed/(2*PI*r))*(2*PI)
    t=p_to_g_ang
    if abs(dist-r)<=0.5:#basically on the orbit
        print("Orbit Phase")
        t+=ang_increase
        gunner_x=r*math.cos(t)+center_x
        gunner_y=r*math.sin(t)+center_y
    elif abs(dist-r)<10:#within the vicinity of orbit
        print("Go to Orbit Phase")
        gunner_x=r*math.cos(t)+center_x
        gunner_y=r*math.sin(t)+center_y
    elif dist>r:#far from orbit
        print("Rush Phase")
        gunner_x+=gunner_speed*math.cos(g_to_p_ang)
        gunner_y+=gunner_speed*math.sin(g_to_p_ang)
    elif dist<r:#far inside of orbit
        print("Run Phase")
        gunner_x+=gunner_speed*math.cos(p_to_g_ang)
        gunner_y+=gunner_speed*math.sin(p_to_g_ang)
    if gunner_x<10:
        gunner_x=10
    if gunner_x>790:
        gunner_x=790
    if gunner_y<10:
        gunner_y=10
    if gunner_y>790:
        gunner_y=790
    canvas.coords(gunner, gunner_x-10, gunner_y-10, gunner_x+10, gunner_y+10)
    root.after(100, gunner_check)

#player movement
def movement():
    global keypress_list, speed, center_x, center_y, speed, safe_circle, r, player
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
    if center_x>790:
        center_x=790
    elif center_x<10:
        center_x=10
    if center_y>790:
        center_y=790
    elif center_y<10:
        center_y=10
    canvas.coords(safe_circle, center_x-r, center_y-r, center_x+r, center_y+r)
    canvas.coords(player, center_x-10, center_y-10, center_x+10, center_y+10)
    root.after(100, movement)

#tkinter canvas
root=tk.Tk()
canvas=tk.Canvas(root, height=800, width=800)
root.resizable(False, False)

#player stats
center_x=400
center_y=400
speed=10
r=100

#gunner stats
gunner_x=10
gunner_y=10
gunner_speed=5

#creating widgets
player=canvas.create_rectangle(center_x-10, center_y-10, center_x+10, center_y+10)
gunner=canvas.create_rectangle(gunner_x-10, gunner_y-10, gunner_x+10, gunner_y+10)
safe_circle=canvas.create_oval(center_x-r, center_y-r, center_x+r, center_y+r)

#keyboard input
keypress_list=[]
listener=keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

#initialize
canvas.pack()
root.after(100,gunner_check)
root.after(100, movement)
root.mainloop()
