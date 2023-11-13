import tkinter as tk
import sqlite3
from data.expense import Expense
from data.dataLabel import DataLabel

class DataViewFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        QUERY = "SELECT *, oid FROM expenses"
        data = {}

        try:  
            # Connect to the database
            # @Diyar: 4-create-concise-variable-list
            # @Diyar: 5-programmatically-create-db-when-needed: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
            conn = sqlite3.connect( 'expenseDatabase.db' )
            c = conn.cursor()

            # Insert into table
            # @Diyar: 4-create-concise-variable-list: in this case for expenses
            c.execute( "SELECT *, oid FROM expenses" )
            expenses = c.fetchall()

            conn.commit()

            # Last element is always the OID and so we map OID's to expense entries
            for expense in expenses:
                data[ expense[-1] ] = Expense( expense[0], expense[1], str( expense[2] ), expense[3] )

        except Exception as err:
            print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

        finally:
            conn.close()

        # oid may not necessarily be ordered correctly, need dataItemCounter to place elements
        self.dataItemCounter = 0
        for oid, expense in data.items():
            dataLabel = DataLabel( self, expense )
            dataLabel.grid( row=self.dataItemCounter, column=0 )

            dataLabelDeleteButton = tk.Button( self, text="Delete Expense" )
            dataLabelDeleteButton.grid( row=self.dataItemCounter, column=1 )
            dataLabelDeleteButton.config( command=lambda label=dataLabel, button=dataLabelDeleteButton, oid=oid: self.deleteExpenseFromDatabase(label, button, oid) )

            self.dataItemCounter += 1

    def addExpenseToDatabase( self, expense ):
        QUERY = "INSERT INTO expenses VALUES (:date, :category, :cost, :description)"

        try:
            # Connect to the database
            # @Diyar: 4-create-concise-variable-list
            # @Diyar: 5-programmatically-create-db-when-needed: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
            conn = sqlite3.connect( 'expenseDatabase.db' )
            c = conn.cursor()

            # Insert into table
            # @Diyar: 4-create-concise-variable-list: in this case for expenses
            c.execute( QUERY, 
                      {   'date': expense.date,
                          'category': expense.category,
                          'cost': expense.cost,
                          'description': expense.description } )
            conn.commit()
            last_inserted_oid = c.lastrowid

            # Create element in UI
            dataLabel = DataLabel( self, expense )
            dataLabel.grid( row=self.dataItemCounter, column=0 )

            dataLabelDeleteButton = tk.Button( self, text="Delete Expense" )
            dataLabelDeleteButton.grid( row=self.dataItemCounter, column=1 )
            dataLabelDeleteButton.config( command=lambda label=dataLabel, button=dataLabelDeleteButton, oid=last_inserted_oid: self.deleteExpenseFromDatabase(label, button, oid) )

            self.dataItemCounter += 1
            
        except Exception as err:
            print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

        finally:
            conn.close()
    

    def deleteExpenseFromDatabase( self, label, button, oid ):
        QUERY = "DELETE from expenses WHERE oid=" + str( oid )

        try:
            # @Diyar: 4-create-concise-variable-list
            conn = sqlite3.connect( 'expenseDatabase.db' )
            c = conn.cursor()

            # Delete from table
            c.execute( QUERY )

            conn.commit()

            # Remove the row from UI only if we successfully deleted from the database
            label.destroy()
            button.destroy()

        except Exception as err:
            print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

        finally:
            conn.close()
            
