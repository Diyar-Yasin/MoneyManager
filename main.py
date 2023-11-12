import tkinter as tk

class MainApplication( tk.Frame ):
    def createGrid( self ):
        # Create top and bottom rows with equal weight
        self.rowconfigure( 0, weight=3 )
        self.rowconfigure( 1, weight=2 )

        # Have the top row contain 3 columns while the bottom row spans all 3 columns
        TOP_COLS = 3
        for i in range( TOP_COLS ):
            self.columnconfigure( i, weight=1 )

        # Setup frames of top row
        pieGraphWidget = tk.Frame( self, bg="orange" )
        timeGraphWidget = tk.Frame( self, bg="blue" )
        addItemAndToolbarWidget = tk.Frame( self, bg="pink" )

        pieGraphWidget.grid( row=0, column=0, sticky="nsew" )
        addItemAndToolbarWidget.grid( row=0, column=1, sticky="nsew" )
        timeGraphWidget.grid( row=0, column=2, sticky="nsew" )

        # Setup frame of bottom to span all 3 columns
        dataViewFrame = tk.Frame(self, bg="green")
        dataViewFrame.grid( row=1, column=0, columnspan=3, sticky="nsew" )

    def __init__( self, parent, *args, **kwargs ):
        tk.Frame.__init__( self, parent, *args, **kwargs )
        self.parent = parent
        
        # Setup window
        self.parent.title( 'Money Manager' )
        self.parent.iconbitmap( './images/appIcon.ico' )

        # Setup grid structure
        self.createGrid()


if __name__ == "__main__":
    root = tk.Tk()    
    MainApplication(root).pack( side="top", fill="both", expand=True )
    root.mainloop()

