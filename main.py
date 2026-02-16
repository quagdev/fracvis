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

    def calculate(self, x, y, itr):
        c = complex(x, y)
        z = complex(0, 0)   

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        return itr - 1
    
    def draw(self):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

        x_start, y_start = -2, -1.5
        width, height = 3, 3
        density = 100

        re = np.linspace(x_start, x_start + width, int(width * density))
        im = np.linspace(y_start, y_start + height, int(height * density))
        X = np.empty((len(re), len(im)))

        for i in range(len(re)):
            for j in range(len(im)):
                X[j, i] = self.calculate(re[i], im[j], self.threshold)
        
        fig.patch.set_facecolor('black')
        ax.imshow(X, interpolation="bicubic", cmap='magma', extent=[x_start, x_start + width, y_start, y_start + height],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        if self.threshold < 10:
            self.threshold += 1
        else:
            self.threshold = int(self.threshold * 1.5)

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

    def calculate(self, zx, zy, cx, cy, itr):
        z = complex(zx, zy)
        c = complex(cx, cy)   

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        return itr - 1
    
    def draw(self):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

        x_start, y_start = -2, -2
        width, height = 4, 4
        density = 50

        re = np.linspace(x_start, x_start + width, int(width * density))
        im = np.linspace(y_start, y_start + height, int(height * density))
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
        ax.imshow(X, interpolation="bicubic", cmap='gray', extent=[x_start, x_start + width, y_start, y_start + height],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        self.threshold += 1

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

label = tk.Label(root, text="FRACVIS", font=("Helvetica Neue", 28, "bold"), bg="#222831", fg="#FFFFFF", pady=10)
label.pack(fill="x")

left_frame = tk.Frame(root, width=50, bg='#222831')
center_frame = tk.Frame(root, bg='#222831')
right_frame = tk.Frame(root, width=50, bg='#222831')

left_frame.pack(side=tk.LEFT, fill=tk.Y)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame.pack(side=tk.LEFT, fill=tk.Y)

canvas = FigureCanvasTkAgg(fig, master = center_frame)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=0, pady=0)
canvas.get_tk_widget().config(bd=0, highlightthickness=0)

root.icon_zoom_in = load_icon("zoom-in.png")
root.icon_zoom_out = load_icon("zoom-out.png")
root.icon_reset = load_icon("equal.png")

Button(left_frame, image=root.icon_zoom_in, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)
Button(left_frame, image=root.icon_zoom_out, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)
Button(left_frame, image=root.icon_reset, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)

root.icon_info = load_icon("info.png")
root.icon_theme = load_icon("theme.png")
root.icon_wall = load_icon("wallpaper.png")
root.icon_anim = load_icon("animation.png")

Button(right_frame, image=root.icon_info, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_theme, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_wall, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)
Button(right_frame, image=root.icon_anim, bd=0, command=lambda: None, height=40, width=40,bg="#3D3D3D").pack(expand=True, padx=10, pady=1)

Button(center_frame, text="Mandelbrot", command=mandelbrot.draw, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#3D3D3D",fg="#F3F4F4").pack(side="left", padx=10, pady=10)
Button(center_frame, text="Julia", command=julia.draw, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#3D3D3D",fg="#F3F4F4").pack(side="left", padx=10)
Button(center_frame, text="Quit", command=root.destroy, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#3D3D3D",fg="#F3F4F4").pack(side="right",padx=10)
Button(center_frame, text="Clear", command=lambda: [ax.clear(), ax.set_xticks([]), ax.set_yticks([]), canvas.draw(),], font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#3D3D3D", fg="#F3F4F4").pack(side="right", padx=10)

root.mainloop()