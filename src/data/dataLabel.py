import tkinter as tk

# Data
from data.expense import Expense

# Styles
from styles.colors import getBackgroundColor, getForegroundColor

class DataLabel( tk.Frame ):
    def __init__(self, parent, expense: Expense):
        super().__init__(parent)

        self.config( bg=getBackgroundColor() )
        
        dateLabel = tk.Label( self, text=expense.day, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        dateLabel.grid( row=0, column=0, sticky="w", padx=5 )

        categoryLabel = tk.Label( self, text=expense.category, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        categoryLabel.grid( row=0, column=1, sticky="w", padx=10 )

        costLabel = tk.Label( self, text=expense.cost, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        costLabel.grid( row=0, column=2, sticky="w", padx=10 )

        descriptionLabel = tk.Label( self, text=expense.description, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=100, anchor="w" )
        descriptionLabel.grid( row=0, column=3, sticky="w", padx=10 )