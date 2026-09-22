class Build:
    def __init__(self, year=None, city= None, number=1):
        self.year = year
        self.city  = city
        self.number = number
        self.get_info()

    def get_info(self):
        print("Year:", self.year, " City:", self.city, " Number:", self.number, sep="")


class School(Build):
    def __init__(self, year=None, city=None, number=1, pupils=0):
        self.pupils = pupils
        super().__init__(year, city, number)

    def get_info(self):
        super().get_info()
        print("Pupils:", self.pupils, sep="")



school1 = School(1971, "Zoria", 221, 500)
# house = Build(1975, "Zoria", 221)
# shop = Build(1955, "Dubno", 52)
