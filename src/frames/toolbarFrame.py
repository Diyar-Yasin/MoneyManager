import tkinter as tk

class ToolbarFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Add your frame-specific logic here
        label = tk.Label(self, text="ToolbarFrame")
        label.pack()

    def getCurrentYear( self ):
        return "2023"
    
    def getCurrentMonth( self ):
        return "11"