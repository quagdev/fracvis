import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

class Mandelbrot():
    #Zn+1 = Zn2 + C
    def calculate(self, x, y, itr):
        c = complex(x, y)
        z = complex(0, 0)

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        
        return itr - 1
    
    def animate():
        return 0




root = tk.Tk()
root.title("Fractals")

fig, ax = plt.subplots(figsize=(3, 2))

frame = tk.Frame(root)
label = tk.Label(font=("Courier", 32), text="fractal")
label.pack()    

canvas = FigureCanvasTkAgg(fig, master = root)
canvas.get_tk_widget().pack()

frame.pack(pady=10)

tk.Button(frame, text="Mandelbrot", command=Mandelbrot.animate, font=("Courier"), width = 10, height = 2).pack(side="left", padx=10)
tk.Button(frame, text="Quit", command=root.destroy, font=("Courier"), width = 10, height = 2).pack(side="right",padx=10)

root.mainloop()