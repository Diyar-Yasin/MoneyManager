import tkinter as tk
import datetime
import re

# Data imports
from data.expense import Expense

class AddItemFrame( tk.Frame ):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        dateLabel = tk.Label( self, text="Date" )
        self.dateInput = tk.Entry( self, width=30, highlightbackground = "red", highlightcolor= "red" )
        self.dateInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.dateInputErrorLabel = tk.Label( self, text="", foreground="red" )
        dateLabel.grid( row=0, column=0 )
        self.dateInput.grid( row=0, column=1 )
        self.dateInputErrorLabel.grid( row=0, column=2 )

        categoryLabel = tk.Label( self, text="Category" )
        self.categoryInput = tk.Entry( self, width=30, highlightbackground = "red", highlightcolor= "red" )
        self.categoryInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.categoryInputErrorLabel = tk.Label( self, text="", foreground="red" )
        categoryLabel.grid( row=1, column=0 )
        self.categoryInput.grid( row=1, column=1 )
        self.categoryInputErrorLabel.grid( row=1, column=2 )

        costLabel = tk.Label( self, text="Cost" )
        self.costInput = tk.Entry( self, width=30, highlightbackground = "red", highlightcolor= "red" )
        self.costInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.costInputErrorLabel = tk.Label( self, text="", foreground="red" )
        costLabel.grid( row=2, column=0 )
        self.costInput.grid( row=2, column=1 )
        self.costInputErrorLabel.grid( row=2, column=2 )

        descriptionLabel = tk.Label( self, text="Description" )
        self.descriptionInput = tk.Entry( self, width=30, highlightbackground = "red", highlightcolor= "red" )
        self.descriptionInput.bind( "<FocusIn>", self.handleAnyInputFocus )
        self.descriptionInputErrorLabel = tk.Label( self, text="", foreground="red" )
        descriptionLabel.grid( row=3, column=0 )
        self.descriptionInput.grid( row=3, column=1 )
        self.descriptionInputErrorLabel.grid( row=3, column=2 )

        self.submitButton = tk.Button( self, text="Enter item", command=self.submitToDatabase )
        self.submitButton.grid( row=4, column=0 )
        

    # Reset all error messages
    def resetAllErrorMessages( self ):
        self.dateInput.config( highlightthickness=0 )
        self.dateInputErrorLabel.config( text="" )

        self.categoryInput.config( highlightthickness=0 )
        self.categoryInputErrorLabel.config( text="" )

        self.costInput.config( highlightthickness=0 )
        self.costInputErrorLabel.config( text="" )

        self.descriptionInput.config( highlightthickness=0 )
        self.descriptionInputErrorLabel.config( text="" )

    # Reset any error messages on focus of an Entry element
    def handleAnyInputFocus( self, event ):
        if event.widget == self.dateInput:
            self.dateInput.config( highlightthickness=0 )
            self.dateInputErrorLabel.config( text="" )

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
        ACCEPTED_DATE_FORMATS = [ '%Y-%m-%d', '%m/%d']

        validDate = False
        for DATE_FORMAT in ACCEPTED_DATE_FORMATS:
            try:
                datetime.datetime.strptime( expense.date, DATE_FORMAT ) # Throws if cannot validate the date
                validDate = True
                break                                                   # As long as one format is valid, we have a valid date
            except ValueError:
                continue
        
        PRICE_FORMAT = r'\d+(?:\.\d{1,2})?'

        validInput = True
        
        if not validDate:
            self.dateInput.config( highlightthickness=1 )
            self.dateInputErrorLabel.config( text="Please input a valid date: YYYY-MM-DD or MM/DD" )
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
        expense = Expense( date=self.dateInput.get(), category=self.categoryInput.get(), cost=self.costInput.get(), description=self.descriptionInput.get() )
        
        self.resetAllErrorMessages()

        if not self.isValidInput( expense ):  
            return
        
        # @Diyar: This is a confusing way to get access to siblings in my UI structure...
        self.parent.parent.dataViewWidget.addExpenseToDatabase( expense )

        # Clear text boxes
        self.dateInput.delete( 0, tk.END )
        self.categoryInput.delete( 0, tk.END )
        self.costInput.delete( 0, tk.END )
        self.descriptionInput.delete( 0, tk.END )