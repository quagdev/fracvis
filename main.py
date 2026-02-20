import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image
from pathlib import Path
import os

class Mandelbrot():
    #Zn+1 = Zn2 + C
    def __init__(self):
        self.threshold = 1
        self.icon_zoom_in = load_icon("zoom-in.png")
        self.icon_zoom_out = load_icon("zoom-out.png")
        self.icon_equal = load_icon("equal.png")
        self.icon_theme = load_icon("theme.png")
        self.icon_wallpaper = load_icon("wallpaper.png")
        self.icon_animation = load_icon("animation.png")
        self.info = load_icon("info.png")
        self.x0, self.y0 = -2, -1.5        
        self.w, self.h  = 3, 3       
        self.orig = (self.x0, self.y0, self.w, self.h)
        self.zoom_factor = 1.2               

    def calculate(self, x, y, itr):
        c = complex(x, y)
        z = complex(0, 0)   

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        return itr - 1
    
    def draw(self):
        global current
        current = mandelbrot

        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

        density = 150

        re = np.linspace(self.x0, self.x0 + self.w, int(self.w * density))
        im = np.linspace(self.y0, self.y0 + self.h, int(self.h * density))
        X = np.empty((len(re), len(im)))

        for i in range(len(re)):
            for j in range(len(im)):
                X[j, i] = self.calculate(re[i], im[j], self.threshold)
        
        fig.patch.set_facecolor('black')
        ax.imshow(X, interpolation="bicubic", cmap='gray', extent=[self.x0, self.x0 + self.w, self.y0, self.y0 + self.h],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        self.threshold += 1

    def zoom(self, factor):
        cx = self.x0 + self.w/2
        cy = self.y0 + self.h/2
        self.w *= factor
        self.h *= factor
        self.x0 = cx - self.w/2
        self.y0 = cy - self.h/2

        self.threshold -= 1
        self.draw()
    
    def reset_view(self):
        self.x0, self.y0, self.w, self.h = self.orig

        if self.threshold < 10:
            self.threshold -= 1
        else:
            self.threshold / 1.5
        self.draw()

class Julia():
    #Zn+1 = Zn2 + K
    def __init__(self):
        self.threshold = 1
        self.icon_zoom_in = load_icon("zoom-in.png")
        self.icon_zoom_out = load_icon("zoom-out.png")
        self.icon_equal = load_icon("equal.png")
        self.icon_theme = load_icon("theme.png")
        self.icon_wallpaper = load_icon("wallpaper.png")
        self.icon_animation = load_icon("animation.png")
        self.info = load_icon("info.png")
        self.x0, self.y0 = -1.5, -1.5        
        self.w, self.h  = 3, 3       
        self.orig = (self.x0, self.y0, self.w, self.h)
        self.zoom_factor = 1.2         

    def calculate(self, zx, zy, cx, cy, itr):
        z = complex(zx, zy)
        c = complex(cx, cy)   

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        return itr - 1
    
    def draw(self):
        global current
        current = julia

        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

        density = 150

        re = np.linspace(self.x0, self.x0 + self.w, int(self.w * density))
        im = np.linspace(self.y0, self.y0 + self.h, int(self.h * density))
        X = np.empty((len(re), len(im)))

        r = 0.7885
        a = np.linspace(0, 2*np.pi, 60)
        if self.threshold >= 60:
            self.threshold = 0
        cx, cy = r * np.cos(a[self.threshold]), r * np.sin(a[self.threshold])

        for i in range(len(re)):
            for j in range(len(im)):
                X[j, i] = self.calculate(re[i], im[j], cx, cy, self.threshold)
        fig.patch.set_facecolor('black')
        ax.imshow(X, interpolation="bicubic", cmap='gray', extent=[self.x0, self.x0 + self.w, self.y0, self.y0 + self.h],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        self.threshold += 1


    
    def zoom(self, factor):
        cx = self.x0 + self.w/2
        cy = self.y0 + self.h/2
        self.w *= factor
        self.h *= factor
        self.x0 = cx - self.w/2
        self.y0 = cy - self.h/2

        self.threshold -= 1
        self.draw()
    
    def reset_view(self):
        self.x0, self.y0, self.w, self.h = self.orig

        self.threshold -= 1
        self.draw()

def load_icon(filename):
    icon_folder = Path(__file__).parent / "icons"
    icon_path = icon_folder / filename

    image = Image.open(icon_path)
    image = image.resize((32,32))
    photo_image = ImageTk.PhotoImage(image)

    return photo_image

root = tk.Tk()
root.title("Fractal Visualizer by quagdev")

fig, ax = plt.subplots(figsize=(3, 2.5))
ax.set_xticks([])
ax.set_yticks([])
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
mandelbrot = Mandelbrot()
julia = Julia()
current = mandelbrot

label = tk.Label(root, text="FRACVIS", font=("Helvetica Neue", 28, "bold"), bg="#E8E8E8", fg="#222831", pady=10)
label.pack(fill="x")

left_frame = tk.Frame(root, width=50, bg='#E8E8E8')
center_frame = tk.Frame(root, bg='#E8E8E8')
right_frame = tk.Frame(root, width=50, bg='#E8E8E8')

left_frame.pack(side=tk.LEFT, fill=tk.Y)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame.pack(side=tk.LEFT, fill=tk.Y)

canvas = FigureCanvasTkAgg(fig, master = center_frame)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=0, pady=0)
canvas.get_tk_widget().config(bd=0, highlightthickness=0)

root.icon_zoom_in = load_icon("zoom-in.png")
root.icon_zoom_out = load_icon("zoom-out.png")
root.icon_reset = load_icon("equal.png")

Button(left_frame, image=root.icon_zoom_in, bd=0, command=lambda: current.zoom(1/current.zoom_factor), height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
Button(left_frame, image=root.icon_zoom_out, bd=0, command=lambda: current.zoom(current.zoom_factor), height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
Button(left_frame, image=root.icon_reset, bd=0, command=lambda: current.reset_view(), height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)

root.icon_info = load_icon("info.png")
root.icon_theme = load_icon("theme.png")
root.icon_wall = load_icon("wallpaper.png")
root.icon_anim = load_icon("animation.png")

Button(right_frame, image=root.icon_info, bd=0, command=lambda: None, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_theme, bd=0, command=lambda: None, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_wall, bd=0, command=lambda: None, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_anim, bd=0, command=lambda: None, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)

Button(center_frame, text="Mandelbrot", command=mandelbrot.draw, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="left", padx=10, pady=10)
Button(center_frame, text="Julia", command=julia.draw, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="left", padx=10)
Button(center_frame, text="Quit", command=root.destroy, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="right",padx=10)
Button(center_frame, text="Clear", command=lambda: [ax.clear(), ax.set_xticks([]), ax.set_yticks([]), canvas.draw(),], font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8", fg="#222831").pack(side="right", padx=10)

root.mainloop()