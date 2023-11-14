class Expense:
    def __init__(self, day, month, year, category, cost, description):
        self.day = day
        self.month = month
        self.year = year
        self.category = category
        self.cost = cost
        self.description = description

    def __str__(self):
        return f"Date: {self.day}/{self.month}/{self.year}, Category: {self.category}, Cost: {self.cost}, Description: {self.description}"

