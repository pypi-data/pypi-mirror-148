class Total:
    
    def __init__(self):
        pass
    
    def add_total(self, list):
        total = list
        for num in list:
            total = total + num
        return total
    