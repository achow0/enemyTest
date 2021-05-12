import math
import tkinter as tk
from pynput import keyboard
class Application:
    def __init__(self, master, height = 800, width = 800, updatesPerSecond = 10):
        self.height = height
        self.width = width
        self.root = master
        self.updatesPerSecond = updatesPerSecond
        self.player = Player()
        self.enemy = Enemy()
        self.canvas = tk.Canvas(self.root, height = self.height, width = self.width)
        self.canvas.pack()
        self.player_rectangle = self.canvas.create_rectangle(self.player.x-self.player.length/2, self.player.y-self.player.length/2, self.player.x+self.player.length/2, self.player.y+self.player.length/2)
        self.enemy_rectangle = self.canvas.create_rectangle(self.enemy.x-self.enemy.length/2, self.enemy.y-self.enemy.length/2, self.enemy.x+self.enemy.length/2, self.enemy.y+self.enemy.length/2)
        self.safe_circle = self.canvas.create_oval(self.player.x-self.enemy.safe_distance, self.player.y-self.enemy.safe_distance, self.player.x+self.enemy.safe_distance, self.player.y+self.enemy.safe_distance)
        self.keypress_list = []
        self.listener = keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
        self.listener.start()
        self.player_movement()
        self.enemy_movement()
    def player_movement(self):
        if "down" in self.keypress_list:
            self.player.update_y(self.player.speed)
        if "up" in self.keypress_list:
            self.player.update_y(-self.player.speed)
        if "left" in self.keypress_list:
            self.player.update_x(-self.player.speed)
        if "right" in self.keypress_list:
            self.player.update_x(self.player.speed)
        self.player.boundary_check(self.height, self.width)
        self.canvas.coords(self.player_rectangle, self.player.x-self.player.length/2, self.player.y-self.player.length/2, self.player.x+self.player.length/2, self.player.y+self.player.length/2)
        self.canvas.coords(self.safe_circle, self.player.x-self.enemy.safe_distance, self.player.y-self.enemy.safe_distance, self.player.x+self.enemy.safe_distance, self.player.y+self.enemy.safe_distance)
        self.root.after(1000//self.updatesPerSecond, self.player_movement)
    def enemy_movement(self):
        self.enemy.update_pos(self.player)
        self.enemy.boundary_check(self.height, self.width)
        self.canvas.coords(self.enemy_rectangle, self.enemy.x-self.enemy.length/2, self.enemy.y-self.enemy.length/2, self.enemy.x+self.enemy.length/2, self.enemy.y+self.enemy.length/2)
        self.root.after(1000//self.updatesPerSecond, self.enemy_movement)
    def key_test(self, key):
        try:
            return key.name
        except:
            return
    def on_press(self, key):
        key = self.key_test(key)
        if not key in self.keypress_list:
            self.keypress_list.append(key)
    def on_release(self, key):
        key = self.key_test(key)
        self.keypress_list.remove(key)

class SimObject:
    def __init__(self, x, y, speed, length):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = length
    def boundary_check(self, height, width):
        if self.x - self.length/2 < 0:
            self.x = self.length/2
        if self.y - self.length/2 < 0:
            self.y = self.length/2
        if self.x + self.length/2 > width:
            self.x = width - self.length/2
        if self.y + self.length/2 > height:
            self.y = height - self.length/2
    def update_x(self, offset):
        self.x+=offset
    def update_y(self, offset):
        self.y+=offset

class Player(SimObject):
    def __init__(self, x = 400, y = 400, speed = 10, length = 20):
        super().__init__(x, y, speed, length)

class Enemy(SimObject):
    def __init__(self, x = 10, y = 10, speed = 5, length = 20, safe_distance = 100):
        super().__init__(x, y, speed, length)
        self.safe_distance = safe_distance
        self.last_phase = -1
    def update_phase(self, n):
        phase_list=[f"{i} Phase" for i in ["Orbit", "Rush", "Run"]]
        if self.last_phase!=n:
            print(phase_list[n])
            self.last_phase = n
    def update_pos(self, player):
        PI=math.pi
        dx=player.x-self.x
        dy=player.y-self.y
        g_to_p_ang=math.atan2(dy,dx)
        p_to_g_ang=PI+g_to_p_ang
        dist=math.sqrt(dx*dx+dy*dy)
        ang_increase=self.speed/self.safe_distance
        t=p_to_g_ang
        if abs(dist-self.safe_distance)<=self.speed:#near the orbit
            self.update_phase(0)
            t+=ang_increase
            self.x=self.safe_distance*math.cos(t)+player.x
            self.y=self.safe_distance*math.sin(t)+player.y
        elif dist>self.safe_distance:#far from orbit
            self.update_phase(1)
            self.update_x(self.speed*math.cos(g_to_p_ang))
            self.update_y(self.speed*math.sin(g_to_p_ang))
        elif dist<self.safe_distance:#far inside of orbit
            self.update_phase(2)
            self.update_x(self.speed*math.cos(p_to_g_ang))
            self.update_y(self.speed*math.sin(p_to_g_ang))


root = tk.Tk()
root.resizable(0,0)
root.title("Enemy Movement Test")
application = Application(root)
tk.mainloop()
