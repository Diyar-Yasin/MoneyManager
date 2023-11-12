import tkinter as tk

class DataViewFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Add your frame-specific logic here
        label = tk.Label(self, text="DataViewFrame")
        label.pack()
