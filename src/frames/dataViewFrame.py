import tkinter as tk
import sqlite3
from data.expense import Expense
from data.dataLabel import DataLabel

class DataViewFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        BACKDROP_COLOR = "#11001c"
        self.parent = parent
        self.updateDataViewFrameData()

    def reloadData( self ):
        self.clearDataView()
        self.updateDataViewFrameData()

    def clearDataView( self ):
        for widget in self.winfo_children():
            widget.destroy()

    def getLatestData( self ):
        currentYear = self.parent.addItemAndToolbarWidget.toolbarWidget.getCurrentYear()
        currentMonth = self.parent.addItemAndToolbarWidget.toolbarWidget.getCurrentMonth()

        QUERY = "SELECT *, oid FROM expenses WHERE year = %s AND month = %s ORDER BY day" % ( currentYear, currentMonth )
        data = {}

        try:  
            # Connect to the database
            # @Diyar: 4-create-concise-variable-list
            conn = sqlite3.connect( 'expenseDatabase.db' )
            c = conn.cursor()

            # Insert into table
            # @Diyar: 4-create-concise-variable-list: in this case for expenses
            c.execute( QUERY )
            expenses = c.fetchall()

            conn.commit()

            # Last element is always the OID and so we map OID's to expense entries
            for expense in expenses:
                # Expense: day, month, year, category, cost, description
                
                data[ expense[-1] ] = Expense( expense[0], expense[1], expense[2], expense[3], str( expense[4] ), expense[5] )

        except Exception as err:
            print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

        finally:
            conn.close()

        return data
    
    def updateDataViewFrameData( self ):
        data = self.getLatestData()
        # oid may not necessarily be ordered correctly, need dataItemCounter to place elements
        dataItemCounter = 0

        for oid, expense in data.items():
            dataLabel = DataLabel( self, expense )
            dataLabel.grid( row=dataItemCounter, column=0 )

            dataLabelDeleteButton = tk.Button( self, text="Delete Expense" )
            dataLabelDeleteButton.grid( row=dataItemCounter, column=1 )
            dataLabelDeleteButton.config( command=lambda label=dataLabel, button=dataLabelDeleteButton, oid=oid: self.deleteExpenseFromDatabase( label, button, oid ) )

            dataItemCounter += 1


    def addExpenseToDatabase( self, expense ):
        QUERY = "INSERT INTO expenses VALUES (:day, :month, :year, :category, :cost, :description)"

        try:
            # Connect to the database
            # @Diyar: 4-create-concise-variable-list
            conn = sqlite3.connect( 'expenseDatabase.db' )
            c = conn.cursor()

            # Insert into table
            # @Diyar: 4-create-concise-variable-list: in this case for expenses
            c.execute( QUERY, 
                      {   'day': expense.day,
                          'month': expense.month,
                          'year': expense.year,
                          'category': expense.category,
                          'cost': expense.cost,
                          'description': expense.description } )
            conn.commit()

        except Exception as err:
            print( 'Query Failed: %s\nError: %s' % ( QUERY, str( err ) ) )

        finally:
            conn.close()

        # While constantly clearing and recreating the view is an expensive operation, realistically it does not affect UX so until it does this simple solution is great!
        self.reloadData()
        self.parent.pieGraphWidget.reloadData()
        self.parent.timeGraphWidget.reloadData()
    

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
            
