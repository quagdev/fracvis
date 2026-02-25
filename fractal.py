import numpy as np
from pathlib import Path
from PIL import Image, ImageTk


class Mandelbrot():
    def __init__(self):
        self.threshold = 1
        self._suspend_threshold = False
        self.cmap = 'gray'
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
    
    def draw(self, ax, canvas, density=None):
        if density is None:
            density = 150

        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

        re = np.linspace(self.x0, self.x0 + self.w, int(self.w * density))
        im = np.linspace(self.y0, self.y0 + self.h, int(self.h * density))
        X = np.empty((len(re), len(im)))

        for i in range(len(re)):
            for j in range(len(im)):
                X[j, i] = self.calculate(re[i], im[j], self.threshold)
        
        fig = ax.figure
        fig.patch.set_facecolor('black')
        ax.imshow(X, interpolation="bicubic", cmap=self.cmap, extent=[self.x0, self.x0 + self.w, self.y0, self.y0 + self.h],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        if not self._suspend_threshold:
            if self.threshold < 10:
                self.threshold += 1
            else:
                self.threshold = int(self.threshold * 1.5)

    def zoom(self, factor):
        cx = self.x0 + self.w/2
        cy = self.y0 + self.h/2
        self.w *= factor
        self.h *= factor
        self.x0 = cx - self.w/2
        self.y0 = cy - self.h/2
        self._suspend_threshold = True
        self._suspend_threshold = False
    def reset_view(self):
        self.x0, self.y0, self.w, self.h = self.orig
        self._suspend_threshold = True
        self._suspend_threshold = False

class Julia():
    def __init__(self):
        self.threshold = 1
        self._suspend_threshold = False
        self.cmap = 'gray'
        self.x0, self.y0 = -1.5, -1.5        
        self.w, self.h  = 3, 3       
        self.orig = (self.x0, self.y0, self.w, self.h)
        self.zoom_factor = 1.2         
        self._suspend_threshold = False

    def calculate(self, zx, zy, cx, cy, itr):
        z = complex(zx, zy)
        c = complex(cx, cy)   

        for i in range(itr):
            z = z**2 + c
            if abs(z) > 4:
                return i
        return itr - 1
    
    def draw(self, ax, canvas, density=None):
        if density is None: density = 150

        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_position([0, 0, 1, 1])   
        ax.margins(0)

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
        fig = ax.figure
        fig.patch.set_facecolor('black')
        ax.imshow(X, interpolation="bicubic", cmap=self.cmap, extent=[self.x0, self.x0 + self.w, self.y0, self.y0 + self.h],  aspect='auto')
        ax.text(0.05, 0.95, f"Iterations: {self.threshold}", transform=ax.transAxes, color="white", fontsize=5, fontweight='bold',verticalalignment='top',bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
        canvas.draw()

        if not self._suspend_threshold:
            self.threshold += 1

    
    def zoom(self, factor):
        cx = self.x0 + self.w/2
        cy = self.y0 + self.h/2
        self.w *= factor
        self.h *= factor
        self.x0 = cx - self.w/2
        self.y0 = cy - self.h/2

        self._suspend_threshold = True
        self._suspend_threshold = False

    def reset_view(self):
        self.x0, self.y0, self.w, self.h = self.orig
        self._suspend_threshold = True
        self._suspend_threshold = False

def load_icon(filename):
    icon_folder = Path(__file__).parent / "icons"
    icon_path = icon_folder / filename

    image = Image.open(icon_path)
    image = image.resize((32,32))
    photo_image = ImageTk.PhotoImage(image)

    return photo_image



def compute_fractal(obj, width_px, height_px, iterations):
    re = np.linspace(obj.x0, obj.x0 + obj.w, width_px, dtype=np.float32)
    im = np.linspace(obj.y0, obj.y0 + obj.h, height_px, dtype=np.float32)
    if isinstance(obj, Mandelbrot):
        C = re + im[:, None] * 1j
        Z = np.zeros_like(C, dtype=np.complex64)
        M = np.full(C.shape, iterations, dtype=np.float32)
        for i in range(iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            escaped = mask & (np.abs(Z) > 2)
            M[escaped] = i
        return M
    else:
        r = 0.7885
        a = np.linspace(0, 2 * np.pi, 60)
        idx = iterations % 60
        c = r * np.cos(a[idx]) + 1j * (r * np.sin(a[idx]))
        Z = re + im[:, None] * 1j
        M = np.full(Z.shape, iterations, dtype=np.float32)
        for i in range(iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] * Z[mask] + c
            escaped = mask & (np.abs(Z) > 2)
            M[escaped] = i
        return M