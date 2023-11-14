import tkinter as tk
from data.expense import Expense

class DataLabel( tk.Frame ):
    def __init__(self, parent, expense: Expense):
        super().__init__(parent)
        
        dateLabel = tk.Label( self, text=expense.day )
        dateLabel.grid( row=0, column=0 )

        categoryLabel = tk.Label( self, text=expense.category )
        categoryLabel.grid( row=0, column=1 )

        costLabel = tk.Label( self, text=expense.cost )
        costLabel.grid( row=0, column=2 )

        descriptionLabel = tk.Label( self, text=expense.description )
        descriptionLabel.grid( row=0, column=3 )