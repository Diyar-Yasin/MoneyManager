import tkinter as tk
import calendar

# Math
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

# Data
from data.expense import Expense

# Styles
from styles.colors import getBackgroundColor

# @Diyar: 14-add-time-graph
class TimeGraphFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.reloadData()
        
    def clearDataView( self ):
        for widget in self.winfo_children():
            widget.destroy()

    def getNumberOfDaysInMonth( self, year, month ):
        return calendar.monthrange( year, month )[1]
    
    def reloadData( self ):
        self.clearDataView()
        
        # the figure that will contain the plot
        fig = Figure( figsize=(2, 2), facecolor=getBackgroundColor() ) 

        # Grab data from dataViewFrame
        data = self.parent.dataViewWidget.getLatestData()

        currentYear = self.parent.addItemAndToolbarWidget.toolbarWidget.getCurrentYear()
        currentMonth = self.parent.addItemAndToolbarWidget.toolbarWidget.getCurrentMonth()

        x = range( 1, self.getNumberOfDaysInMonth( int( currentYear ), int( currentMonth ) ) )
        y = [0] * len(x)

        for item in data.items():
            expense: Expense = item[1]

            y[ int( expense.day ) ] += float( expense.cost )

        for i in range( 2, len(y) ):
            y[ i ] += y[ i - 1 ]

        plt = fig.add_subplot(111)
        plt.plot(x, y, 'k,-')
        plt.set_xlabel('Day of the Month', color='white')
        plt.set_ylabel('Money Spent', color='white')
        plt.set_xticks(x)
        plt.set_yticks(np.arange(min(y), max(y) + 1, step=100))
        plt.tick_params(axis='y', labelcolor='white')
        plt.fill_between(x, y, color='black', alpha=0.4)

        # creating the Tkinter canvas containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg( fig, master = self )

        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        
        
