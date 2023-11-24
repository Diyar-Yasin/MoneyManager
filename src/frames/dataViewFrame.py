import tkinter as tk
from tkinter import ttk
import sqlite3

# Data
from data.expense import Expense
from data.dataLabel import DataLabel

# Styles
from styles.colors import getBackgroundColor, getForegroundColor


class DataViewFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
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
    
    # @Diyar: BUG-17-scrollbar-wont-work-until-window-is-resized
    def updateDataViewFrameData( self ):
        # Create a Canvas widget and add a scrollbar
        canvas = tk.Canvas( self, bg=getBackgroundColor(), highlightbackground=getBackgroundColor(), highlightcolor=getBackgroundColor() )

        scrollbar = ttk.Scrollbar( self, orient="vertical", command=canvas.yview )
        canvas.config( yscrollcommand=scrollbar.set )

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        innerFrame = tk.Frame( canvas, bg=getBackgroundColor() )

        innerFrameId = canvas.create_window(0, 0, window=innerFrame, anchor="nw")

        def onCanvasConfigure( event ):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def onFrameConfigure( event ):
            canvas.itemconfig(innerFrameId, width=canvas.winfo_width())
        
        canvas.bind( "<Configure>", onCanvasConfigure )
        innerFrame.bind( "<Configure>", onFrameConfigure )

        # Place the canvas and scrollbar
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Finally get the data
        data = self.getLatestData()

        # oid may not necessarily be ordered correctly, need dataItemCounter to place elements
        dataItemCounter = 0

        for oid, expense in data.items():
            dataLabel = DataLabel( innerFrame, expense )
            dataLabel.grid( row=dataItemCounter, column=0, sticky="w" )

            dataLabelDeleteButton = tk.Button( innerFrame, text="Delete Expense", width=20, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor() )
            dataLabelDeleteButton.grid( row=dataItemCounter, column=1, sticky="e", pady=5 )
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
            
