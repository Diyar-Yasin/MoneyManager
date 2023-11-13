import tkinter as tk

# Frame imports
from frames.addItemFrame import AddItemFrame
from frames.toolbarFrame import ToolbarFrame

class AddItemAndToolbarFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Setup frame structure
        self.rowconfigure( 0, weight=1 )
        self.rowconfigure( 1, weight=5 )

        self.columnconfigure( 0, weight=1 )

        self.toolbarWidget = ToolbarFrame( self, bg="black" )
        self.addItemWidget = AddItemFrame( self )

        self.toolbarWidget.grid( row=0, column=0, sticky="nsew" )
        self.addItemWidget.grid( row=1, column=0, sticky="nsew" )
