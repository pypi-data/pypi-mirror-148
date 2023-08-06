class Total:
    
    def __init__(self):
        pass
    
    def add_total(self, list):
        income_total = 0
        expense_total = 0
        arr = []
        for itr in list:
            if 'Income' == itr.get('add_money'):
                income_total = income_total + itr.get('quantity')
            
            elif 'Expense' == itr.get('add_money'):
                expense_total = expense_total + itr.get('quantity')
        arr.append(income_total)
        arr.append(expense_total)
        return arr
    