class Add:
    
    def __init__(self):
        pass
    
    def add(self, car_rent_per_day: int, days: int):
        if days > 4:
            return round(0.8*car_rent_per_day*days, 2)
        elif days > 2:
            return round(0.9*car_rent_per_day*days, 2)
        return  car_rent_per_day*days