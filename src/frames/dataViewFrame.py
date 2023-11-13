import tkinter as tk
import sqlite3
from data.expense import Expense
from data.dataLabel import DataLabel

class DataViewFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # @Diyar: 3-integrate-database-into-data-view
        # Connect to the database
        # @Diyar: 4-create-concise-variable-list
        # @Diyar: 5-programmatically-create-db-when-needed: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
        conn = sqlite3.connect('expenseDatabase.db')
        c = conn.cursor()

        # Insert into table
        # @Diyar: 4-create-concise-variable-list: in this case for expenses
        c.execute("SELECT *, oid FROM expenses")
        expenses = c.fetchall()

        conn.commit()
        conn.close()
        data = []
        for expense in expenses:
            print(expense)
            data.append( Expense( expense[0], expense[1], str( expense[2] ), expense[3] ) )
        
        for i in range( 0, len(data) ):
            dataLabel = DataLabel( self, data[i] )
            dataLabel.grid( row=i, column=0 )
