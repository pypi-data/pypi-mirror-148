class Add:
    
    def __init__(self):
        pass
    
    def add(self, car_rent_per_day: int, days: int):
        if days > 4:
            return 0.9*car_rent_per_day*days
        return  car_rent_per_day*days