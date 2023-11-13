class Expense:
    def __init__(self, date, category, cost, description):
        self.date = date
        self.category = category
        self.cost = cost
        self.description = description

    def __str__(self):
        return f"Date: {self.date}, Category: {self.category}, Cost: {self.cost}, Description: {self.description}"

