import tkinter as tk
import sqlite3

# Frame imports
from frames.addItemAndToolbarFrame import AddItemAndToolbarFrame
from frames.pieGraphFrame import PieGraphFrame
from frames.timeGraphFrame import TimeGraphFrame
from frames.dataViewFrame import DataViewFrame

# Styles
from styles.colors import getBackgroundColor

class MainApplication( tk.Frame ):
    def createGrid( self ):

        # Create top and bottom rows with equal weight
        self.rowconfigure( 0, weight=3 )
        self.rowconfigure( 1, weight=2 )

        # Have the top row contain 3 columns while the bottom row spans all 3 columns
        self.columnconfigure( 0, weight=3 )
        self.columnconfigure( 1, weight=1 )
        self.columnconfigure( 2, weight=3 )

        # Setup frames of top row
        self.addItemAndToolbarWidget = AddItemAndToolbarFrame( self, bg=getBackgroundColor() )
        self.addItemAndToolbarWidget.grid( row=0, column=1, sticky="nsew" )

        # Setup frame of bottom to span all 3 columns
        self.dataViewWidget = DataViewFrame( self, bg=getBackgroundColor() )
        self.dataViewWidget.grid( row=1, column=0, columnspan=3, sticky="nsew" )

        # These top frame rows rely on dataViewWidget and must be initialized last
        self.pieGraphWidget = PieGraphFrame( self )
        self.timeGraphWidget = TimeGraphFrame( self )

        self.pieGraphWidget.grid( row=0, column=0, sticky="nsew" )
        self.timeGraphWidget.grid( row=0, column=2, sticky="nsew" )


    def __init__( self, parent, *args, **kwargs ):
        tk.Frame.__init__( self, parent, *args, **kwargs )
        self.parent = parent
        
        # Setup window
        # @Diyar: 4-create-concise-variable-list
        self.parent.title( 'Money Manager' )
        self.parent.iconbitmap( '../images/appIcon.ico' ) 

        # Setup grid structure
        self.createGrid()


def setupInitialPageGeometry( root ):
    WINDOW_START_WIDTH_PX = 1600
    WINDOW_START_HEIGHT_PX = 1000

    width = WINDOW_START_WIDTH_PX
    height = WINDOW_START_HEIGHT_PX
    root.geometry(f"{width}x{height}")
    root.resizable(width=False, height=False)

def setupDatabaseIfNecessary():
    QUERY = "CREATE TABLE IF NOT EXISTS expenses ( day integer, month integer, year integer, category text, cost real, description text )"

    try:
        conn = sqlite3.connect( 'expenseDatabase.db' )
        c = conn.cursor()

        c.execute( QUERY )
        
        conn.commit()

    except Exception as err:
        print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

    finally:
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()

    setupInitialPageGeometry( root )

    setupDatabaseIfNecessary()

    # Create MainApplication object and begin the runloop
    MainApplication(root).pack( side="top", fill="both", expand=True )
    root.mainloop()

