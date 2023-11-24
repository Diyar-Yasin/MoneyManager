import tkinter as tk
import datetime
import calendar
import re

# Data
from data.expense import Expense

# Styles
from styles.colors import getBackgroundColor, getForegroundColor

class AddItemFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        dayLabel = tk.Label( self, text="Day", font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        self.dayInput = tk.Entry( self, width=30, highlightbackground = "red", bg=getBackgroundColor(), fg=getForegroundColor(), highlightcolor= "red", font="TkFixedFont" )
        self.dayInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.dayInputErrorLabel = tk.Label( self, text="", font="TkFixedFont", foreground="red", bg=getBackgroundColor() )
        dayLabel.grid( row=0, column=0 )
        self.dayInput.grid( row=0, column=1 )
        self.dayInputErrorLabel.grid( row=0, column=2 )

        categoryLabel = tk.Label( self, text="Category", font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        self.categoryInput = tk.Entry( self, width=30, highlightbackground = "red", bg=getBackgroundColor(), fg=getForegroundColor(), highlightcolor= "red", font="TkFixedFont" )
        self.categoryInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.categoryInputErrorLabel = tk.Label( self, text="", font="TkFixedFont", foreground="red", bg=getBackgroundColor() )
        categoryLabel.grid( row=1, column=0 )
        self.categoryInput.grid( row=1, column=1 )
        self.categoryInputErrorLabel.grid( row=1, column=2 )

        costLabel = tk.Label( self, text="Cost", font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        self.costInput = tk.Entry( self, width=30, highlightbackground = "red", bg=getBackgroundColor(), fg=getForegroundColor(), highlightcolor= "red", font="TkFixedFont" )
        self.costInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.costInputErrorLabel = tk.Label( self, text="", font="TkFixedFont", foreground="red", bg=getBackgroundColor() )
        costLabel.grid( row=2, column=0 )
        self.costInput.grid( row=2, column=1 )
        self.costInputErrorLabel.grid( row=2, column=2 )

        descriptionLabel = tk.Label( self, text="Description", font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor(), width=20, anchor="w" )
        self.descriptionInput = tk.Entry( self, width=30, highlightbackground = "red", bg=getBackgroundColor(), fg=getForegroundColor(), highlightcolor= "red", font="TkFixedFont" )
        self.descriptionInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.descriptionInputErrorLabel = tk.Label( self, text="", font="TkFixedFont", foreground="red", bg=getBackgroundColor() )
        descriptionLabel.grid( row=3, column=0 )
        self.descriptionInput.grid( row=3, column=1 )
        self.descriptionInputErrorLabel.grid( row=3, column=2 )

        self.submitButton = tk.Button( self, text="Enter item", command=self.submitToDatabase, width=20, font="TkFixedFont", bg=getBackgroundColor(), fg=getForegroundColor() )
        self.submitButton.grid( row=4, column=0 )
        

    # Reset all error messages
    def resetAllErrorMessages( self ):
        self.dayInput.config( highlightthickness=0 )
        self.dayInputErrorLabel.config( text="" )

        self.categoryInput.config( highlightthickness=0 )
        self.categoryInputErrorLabel.config( text="" )

        self.costInput.config( highlightthickness=0 )
        self.costInputErrorLabel.config( text="" )

        self.descriptionInput.config( highlightthickness=0 )
        self.descriptionInputErrorLabel.config( text="" )

    # Reset any error messages on focus of an Entry element
    def handleAnyInputFocus( self, event ):
        if event.widget == self.dayInput:
            self.dayInput.config( highlightthickness=0 )
            self.dayInputErrorLabel.config( text="" )

        elif event.widget == self.categoryInput:
            self.categoryInput.config( highlightthickness=0 )
            self.categoryInputErrorLabel.config( text="" )

        elif event.widget == self.costInput:
            self.costInput.config( highlightthickness=0 )
            self.costInputErrorLabel.config( text="" )
        
        elif event.widget == self.descriptionInput:
            self.descriptionInput.config( highlightthickness=0 )
            self.descriptionInputErrorLabel.config( text="" )

    
    def isValidInput( self, expense ):
        DATE_FORMAT = '%Y-%m-%d'

        # The user picks the current year and month using the toolbar, they only set the day when adding an expense
        currentYear = self.parent.toolbarWidget.getCurrentYear()
        currentMonth = self.parent.toolbarWidget.getCurrentMonth()
        date = str( currentYear ) + "-" + str( currentMonth ) + "-" + expense.day
        validDate = True

        try:
            datetime.datetime.strptime( date, DATE_FORMAT ) # Throws if cannot validate the date
        except ValueError:
            validDate = False
        
        PRICE_FORMAT = r'\d+(?:\.\d{1,2})?'

        validInput = True
        
        if not validDate:
            NUM_DAYS_IN_MONTH = calendar.monthrange( int( currentYear ), int( currentMonth ) )[1]
            self.dayInput.config( highlightthickness=1 )
            self.dayInputErrorLabel.config( text="Please input a valid day: 1-%s" % ( NUM_DAYS_IN_MONTH ) )
            validInput = False

        if expense.category == "":
            self.categoryInput.config( highlightthickness=1 )
            self.categoryInputErrorLabel.config( text="Please input a category" )
            validInput = False

        if not re.match( PRICE_FORMAT, expense.cost ):
            self.costInput.config( highlightthickness=1 )
            self.costInputErrorLabel.config( text="Please input a valid cost (e.g. 240.12)" )
            validInput = False

        if expense.description == "":
            self.descriptionInput.config( highlightthickness=1 )
            self.descriptionInputErrorLabel.config( text="Please input a description" )
            validInput = False

        return validInput
    
    def submitToDatabase( self ):
        expense = Expense( day=self.dayInput.get(), month=self.parent.toolbarWidget.getCurrentMonth(),
                          year=self.parent.toolbarWidget.getCurrentYear(), category=self.categoryInput.get(), 
                          cost=self.costInput.get(), description=self.descriptionInput.get() )
        
        self.resetAllErrorMessages()

        if not self.isValidInput( expense ):  
            return
        
        # @Diyar: This is a confusing way to get access to siblings in my UI structure...
        self.parent.parent.dataViewWidget.addExpenseToDatabase( expense )

        # Clear text boxes
        self.dayInput.delete( 0, tk.END )
        self.categoryInput.delete( 0, tk.END )
        self.costInput.delete( 0, tk.END )
        self.descriptionInput.delete( 0, tk.END )