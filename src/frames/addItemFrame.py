import tkinter as tk
import sqlite3

class AddItemFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
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
    def isValidInput( self ):
        return True
    
    def submitToDatabase( self ):
        if self.isValidInput():    
            # Connect to the database
            # @Diyar: 4-create-concise-variable-list
            # @Diyar: 5-programmatically-create-db-when-needed: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
            conn = sqlite3.connect('expenseDatabase.db')
            c = conn.cursor()

            # Insert into table
            # @Diyar: 4-create-concise-variable-list: in this case for expenses
            c.execute("INSERT INTO expenses VALUES (:date, :category, :cost, :description)",
                      {
                          'date': self.dateInput.get(),
                          'category': self.categoryInput.get(),
                          'cost': self.costInput.get(),
                          'description': self.descriptionInput.get()
                      })

            conn.commit()
            conn.close()

            # Clear text boxes
            self.dateInput.delete( 0, tk.END )
            self.categoryInput.delete( 0, tk.END )
            self.costInput.delete( 0, tk.END )
            self.descriptionInput.delete( 0, tk.END )
        else:
            # @Diyar: 2-add-input-validation
            return