import matplotlib.pyplot as plt
current = None
theme_open = False

def _pixel_to_delta(obj, dx, dy):
    w_px = canvas.get_tk_widget().winfo_width()
    h_px = canvas.get_tk_widget().winfo_height()
    sx = obj.w / w_px
    sy = obj.h / h_px
    return dx * sx, dy * sy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkmacosx import Button
from PIL import ImageTk, Image
from pathlib import Path
import time

from fractal import Mandelbrot, Julia, load_icon, compute_fractal

def save_wallpaper():
    path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
    if not path:
        return
    def worker():
        width, height = 3840, 2160
        arr = compute_fractal(current, width, height, current.threshold)
        m = arr.max()
        norm = arr / m if m > 0 else arr
        try:
            cmap = plt.get_cmap(current.cmap)
        except Exception:
            cmap = plt.get_cmap('gray')
        rgba = cmap(norm)
        rgba8 = np.uint8(rgba * 255)
        img = Image.fromarray(rgba8)
        img.save(path)
    import threading
    threading.Thread(target=worker, daemon=True).start()


def save_animation():
    path = filedialog.asksaveasfilename(defaultextension='.gif', filetypes=[('GIF', '*.gif')])
    if not path:
        return
    def worker():
        width, height = 3840, 2160
        frames = []
        for itr in range(1, current.threshold + 1):
            arr = compute_fractal(current, width, height, itr)
            m = arr.max()
            norm = arr / m if m > 0 else arr
            try:
                cmap = plt.get_cmap(current.cmap)
            except Exception:
                cmap = plt.get_cmap('gray')
            rgba = cmap(norm)
            rgba8 = np.uint8(rgba * 255)
            frames.append(Image.fromarray(rgba8))
        if frames:
            frames[0].save(path, save_all=True, append_images=frames[1:], duration=50, loop=0)
    import threading
    threading.Thread(target=worker, daemon=True).start()


def info_popup():
    if root is None:
        return
    win = tk.Toplevel(root)
    win.title("Controls")
    win.resizable(False, False)
    win.config(bg="#E8E8E8")
    header = tk.Frame(win, bg="#E8E8E8")
    header.pack(fill='x', pady=2)

    content = tk.Frame(win, bg="#E8E8E8")
    content.pack(padx=10, pady=5)
    items = [
        (root.icon_zoom_in, "Zoom in"),
        (root.icon_zoom_out, "Zoom out"),
        (root.icon_reset, "Reset view"),
        (root.icon_theme, "Choose colour theme"),
        (root.icon_wall, "Save wallpaper (4K)"),
        (root.icon_anim, "Save animation GIF"),
        (root.icon_info, "Show this help")
    ]
    for img, desc in items:
        row = tk.Frame(content, bg="#E8E8E8")
        row.pack(anchor='w', pady=2)
        lbl = tk.Label(row, image=img, bg="#E8E8E8")
        lbl.image = img
        lbl.pack(side='left')
        tk.Label(row, text=desc, font=("Helvetica Neue", 14), bg="#E8E8E8", fg="#222831").pack(side='left', padx=5)


def theme_popup():
    global mandelbrot, julia, current
    if root is None:
        return
    if current:
        old_thresh = current.threshold
        current._suspend_threshold = True
    else:
        old_thresh = None
    cmaps = ["magma", "plasma", "gray", "inferno", "viridis", "Blues", "Greens", "Reds"]
    def make_preview(cmap, w=80, h=20):
        grad = np.linspace(0, 1, w, dtype=np.float32)[None, :]
        try:
            cmap_obj = plt.get_cmap(cmap)
        except Exception:
            try:
                cmap_obj = plt.get_cmap(cmap.capitalize())
            except Exception:
                cmap_obj = plt.get_cmap('gray')
        rgba = cmap_obj(grad)
        rgba8 = np.uint8(rgba * 255)
        img = Image.fromarray(rgba8, mode='RGBA').resize((w, h))
        return ImageTk.PhotoImage(img)

    win = tk.Toplevel(root)
    win.title("Select theme")
    win.resizable(False, False)
    win.config(bg="#E8E8E8")
    def _on_close():
        global theme_open
        if current:
            current._suspend_threshold = False
            if old_thresh is not None:
                current.threshold = old_thresh
        theme_open = False
        win.destroy()
    win.protocol('WM_DELETE_WINDOW', _on_close)
    header = tk.Frame(win, bg="#E8E8E8")
    header.pack(fill='x', pady=2)
    tk.Label(header, text="Pick a colour map", font=("Helvetica Neue", 28, "bold"), bg="#E8E8E8", fg="#222831").pack(side='left', padx=5)

    grid = tk.Frame(win, bg="#E8E8E8")
    grid.pack(padx=10, pady=5)
    previews = {}
    def choose(cmap):
        mandelbrot.cmap = cmap
        julia.cmap = cmap
        if current:
            current.cmap = cmap
            current.draw(ax, canvas)
        _on_close()

    for idx, cmap in enumerate(cmaps):
        img = make_preview(cmap)
        previews[cmap] = img
        rbase = (idx // 4) * 2
        ccol = idx % 4
        btn = tk.Button(grid, image=img, command=lambda c=cmap: choose(c), bg="#E8E8E8", bd=0)
        btn.image = img            
        btn.grid(row=rbase, column=ccol, padx=5, pady=2)
        tk.Label(grid, text=cmap, font=("Helvetica Neue", 12), bg="#E8E8E8", fg="#222831").grid(row=rbase + 1, column=ccol)
    win._previews = previews

last_time = 0

root = None
canvas = None


def on_press(event):
    current._drag_start = (event.x, event.y)
    current._view_start = (current.x0, current.y0)
    current._suspend_threshold = True
def on_motion(event):
    global last_time
    now = time.time()
    if now - last_time < 1/30:
        return
    last_time = now
    dx = event.x - current._drag_start[0]
    dy = event.y - current._drag_start[1]
    ddx, ddy = _pixel_to_delta(current, dx, dy)
    current.x0 = current._view_start[0] - ddx
    current.y0 = current._view_start[1] - ddy
    current.draw(ax, canvas, density=50)

def on_release(event):
    current._suspend_threshold = True
    current.draw(ax, canvas, density=150)
    current._suspend_threshold = False

def animate():
    global theme_open
    if not current._suspend_threshold and not theme_open:
        current.threshold += 1
    current.draw(ax, canvas)
    root.after(30, animate)

if __name__ == "__main__":
    mandelbrot = Mandelbrot()
    julia = Julia()
    current = mandelbrot
    root = tk.Tk()
    root.title("Fractal Visualizer by quagdev")

    fig, ax = plt.subplots(figsize=(3, 2.5))
    ax.set_xticks([])
    ax.set_yticks([])
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

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

    canvas.get_tk_widget().bind("<ButtonPress-1>", on_press)
    canvas.get_tk_widget().bind("<B1-Motion>",   on_motion)
    canvas.get_tk_widget().bind("<ButtonRelease-1>", lambda e: setattr(current, '_suspend_threshold', False))

    def safe_zoom(factor):
        old = current.threshold
        setattr(current, '_suspend_threshold', True)
        current.zoom(factor)
        current.draw(ax, canvas)
        current.threshold = old
        setattr(current, '_suspend_threshold', False)

    def safe_reset():
        old = current.threshold
        setattr(current, '_suspend_threshold', True)
        current.reset_view()
        current.draw(ax, canvas)
        current.threshold = old
        setattr(current, '_suspend_threshold', False)

    def on_scroll(event):
        try:
            delta = event.delta
        except AttributeError:
            delta = 1 if event.num == 4 else -1
        factor = 1/current.zoom_factor if delta > 0 else current.zoom_factor
        safe_zoom(factor)

    canvas.get_tk_widget().bind("<MouseWheel>", on_scroll)
    canvas.get_tk_widget().bind("<Button-4>", on_scroll)
    canvas.get_tk_widget().bind("<Button-5>", on_scroll)

    root.icon_zoom_in = load_icon("zoom-in.png")
    root.icon_zoom_out = load_icon("zoom-out.png")
    root.icon_reset = load_icon("equal.png")

    Button(left_frame, image=root.icon_zoom_in, bd=0,
           command=lambda: safe_zoom(1/current.zoom_factor),
           height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
    Button(left_frame, image=root.icon_zoom_out, bd=0,
           command=lambda: safe_zoom(current.zoom_factor),
           height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
    Button(left_frame, image=root.icon_reset, bd=0,
           command=safe_reset,
           height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)

    root.icon_info = load_icon("info.png")
    root.icon_theme = load_icon("theme.png")
    root.icon_wall = load_icon("wallpaper.png")
    root.icon_anim = load_icon("animation.png")

    Button(right_frame, image=root.icon_info, bd=0, command=lambda: info_popup(), height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
    Button(right_frame, image=root.icon_theme, bd=0,
           command=lambda: [globals().__setitem__('theme_open', True), theme_popup()],
           height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
    Button(right_frame, image=root.icon_wall, bd=0, command=save_wallpaper, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)
    Button(right_frame, image=root.icon_anim, bd=0, command=save_animation, height=40, width=40,bg="#E8E8E8").pack(expand=True, padx=10, pady=1)

    Button(center_frame, text="Mandelbrot", command=lambda: [setattr(mandelbrot, '_suspend_threshold', False), mandelbrot.draw(ax, canvas)], font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="left", padx=10, pady=10)
    Button(center_frame, text="Julia", command=lambda: [setattr(julia, '_suspend_threshold', False), julia.draw(ax, canvas)], font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="left", padx=10)
    Button(center_frame, text="Quit", command=root.destroy, font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8",fg="#222831").pack(side="right",padx=10)
    Button(center_frame, text="Clear", command=lambda: [ax.clear(), ax.set_xticks([]), ax.set_yticks([]), canvas.draw(),], font=("Helvetica Neue", 18, "bold"), width = 120, height = 40, bg="#E8E8E8", fg="#222831").pack(side="right", padx=10)

    root.mainloop()