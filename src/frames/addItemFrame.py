import tkinter as tk
import sqlite3

# Data imports
from data.expense import Expense

class AddItemFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        dateLabel = tk.Label( self, text="Date" )
        self.dateInput = tk.Entry( self, width=30 )
        dateLabel.grid( row=0, column=0 )
        self.dateInput.grid( row=0, column=1 )

        categoryLabel = tk.Label( self, text="Category" )
        self.categoryInput = tk.Entry( self, width=30 )
        categoryLabel.grid( row=1, column=0 )
        self.categoryInput.grid( row=1, column=1 )

        costLabel = tk.Label( self, text="Cost" )
        self.costInput = tk.Entry( self, width=30 )
        costLabel.grid( row=2, column=0 )
        self.costInput.grid( row=2, column=1 )

        descriptionLabel = tk.Label( self, text="Description" )
        self.descriptionInput = tk.Entry( self, width=30 )
        descriptionLabel.grid( row=3, column=0 )
        self.descriptionInput.grid( row=3, column=1 )

        submitButton = tk.Button( self, text="Enter item", command=self.submitToDatabase )
        submitButton.grid( row=4, column=0 )

     # @Diyar: 2-add-input-validation
    def isValidInput( self, expense ):
        return True
    
    def submitToDatabase( self ):
        expense = Expense( date=self.dateInput.get(), category=self.categoryInput.get(), cost=self.costInput.get(), description=self.descriptionInput.get() )
        
        if self.isValidInput( expense ):  
              
            # @Diyar: This is a confusing way to get access to siblings in my UI structure...
            self.parent.parent.dataViewWidget.addExpenseToDatabase( expense )

            # Clear text boxes
            self.dateInput.delete( 0, tk.END )
            self.categoryInput.delete( 0, tk.END )
            self.costInput.delete( 0, tk.END )
            self.descriptionInput.delete( 0, tk.END )
        else:
            # @Diyar: 2-add-input-validation
            return