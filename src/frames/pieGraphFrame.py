import tkinter as tk

# Math
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

# Data
from data.expense import Expense

# Styles
from styles.colors import getBackgroundColor

class PieGraphFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.reloadData()
        
    def clearDataView( self ):
        for widget in self.winfo_children():
            widget.destroy()

    def reloadData( self ):
        self.clearDataView()
        # the figure that will contain the plot
        

        fig = Figure( figsize=(2, 2), facecolor=getBackgroundColor() ) 

        # Grab data from dataViewFrame
        data = self.parent.dataViewWidget.getLatestData()

        costOfEachCategoryDict = {}
        for item in data.items():
            expense: Expense = item[1]

            if expense.category in costOfEachCategoryDict:
                costOfEachCategoryDict[ expense.category ] += float( expense.cost )
            else:
                costOfEachCategoryDict[ expense.category ] = float( expense.cost )


        categories = []
        costOfCategoryArray = []
        for key, value in costOfEachCategoryDict.items():
            categories.append( key )
            costOfCategoryArray.append( value )
        
        costOfCategoryNpArray = np.array( costOfCategoryArray )

        # adding the subplot 
        pieChart = fig.add_subplot(111) 
        explode = [0.05] * len(categories)

        # Color definitions
        GRAPE_HEX_COLOR = "#7209b7"
        ROSE_HEX_COLOR = "#F72585"
        ZAFFRE_HEX_COLOR = "#3a0ca3"
        NEON_BLUE_HEX_COLOR = "#4361ee"

        # plotting the graph 
        pieChart.pie( costOfCategoryNpArray, labels=categories, labeldistance=.4, pctdistance=1.25, 
                     autopct='%1.1f%%', textprops={'size': 'smaller', 'color': 'w'},
                     colors=[ROSE_HEX_COLOR, ZAFFRE_HEX_COLOR, NEON_BLUE_HEX_COLOR, GRAPE_HEX_COLOR], 
                     explode=explode )
    
        # creating the Tkinter canvas containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
    