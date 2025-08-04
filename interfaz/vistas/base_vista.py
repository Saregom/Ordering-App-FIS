import tkinter as tk

class BaseVista:
    def __init__(self, parent):
        self.parent = parent
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
    
    def create_window(self, title, width=600, height=450):
        """Crea una ventana secundaria centrada"""
        win = tk.Toplevel(self.parent)
        win.title(title)
        win.configure(bg="#f0f0f0")
        
        # Centrar la ventana
        centerX = (self.screen_width // 2) - (width // 2)
        centerY = (self.screen_height // 2) - (height // 2 + 100)
        win.geometry(f"{width}x{height}+{centerX}+{centerY}")
        
        return win
