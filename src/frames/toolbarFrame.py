import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Styles
from styles.colors import getBackgroundColor, getForegroundColor

class ToolbarFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        
        self.selectedDateLabel = tk.Label( self, text="Expenses For", font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=12, anchor="w" )
        self.selectedDateLabel.grid( column = 0, row = 15, padx = 10, pady = 25 ) 

        MONTHS = [' January',  
                    ' February', 
                    ' March', 
                    ' April', 
                    ' May', 
                    ' June',  
                    ' July',  
                    ' August',  
                    ' September',  
                    ' October',  
                    ' November',  
                    ' December']
                
        self.monthSelector = ttk.Combobox( self, width = 27, values=MONTHS, state="readonly" )
        self.monthSelector.grid( row = 15, column = 1 ) 

        self.monthSelector.bind( "<<ComboboxSelected>>", self.onNewDateSelected )

        DEFAULT_MONTH = MONTHS[ datetime.now().month - 1 ]
        self.monthSelector.set( DEFAULT_MONTH )

        self.yearSelector = tk.Entry( self, width=30 )
        self.yearSelector.insert(0, str( datetime.now().year ) )
        self.yearSelector.bind( "<FocusOut>", self.onYearSet )
        self.yearSelector.bind( "<Return>", self.onYearSet )
        self.yearSelector.grid( row = 15, column = 2 )


    def onYearSet( self, event ):
        # very simple year validation
        try:
            YEAR_AS_INT = int( self.yearSelector.get() )

            if YEAR_AS_INT < 0 or YEAR_AS_INT > datetime.now().year:
                raise ValueError( "Value must be between 0 and the current year" )
            
        except Exception as err:
            self.yearSelector.delete( 0, tk.END )
            self.yearSelector.insert( 0, str( datetime.now().year ) )

        self.onNewDateSelected()
    
        
    def onNewDateSelected( self, event=None ):
        self.parent.parent.dataViewWidget.reloadData()
        self.parent.parent.pieGraphWidget.reloadData()
        self.parent.parent.timeGraphWidget.reloadData()
    
    def getCurrentYear( self ):
        return self.yearSelector.get()
    
    def getCurrentMonth( self ):
        return self.monthSelector.current() + 1