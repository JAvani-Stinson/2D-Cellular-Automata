#Create a class for te grid
class Grid:
    def __init__(self, max_wid, min_wid, max_len, min_len):
        self.Max_Width = max_wid
        self.Min_Width = min_wid
        self.Max_Length = max_len
        self.Min_Length = min_len
        self.positions = set()
        for i in range(self.Min_Width, self.Max_Width + 1):
            for j in range(self.Min_Length, self.Max_Length + 1):
                self.positions.add((i, j))

#Create a class for the cells by location on grid
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.status = 0
        self.color = "white"
        self.group = ""
        self.grid = ""

    def get_energy(self, cells):
        energy = 0
        if self.status == 100:
            return 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                if a in [-1, 1] or b in [-1, 1]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format(self.i + a, self.j + b)].status == 100:
                                energy -= 40
                            elif cells["{}, {}".format(self.i + a, self.j + b)].status == 0:
                                energy += 0
                            elif cells["{}, {}".format(self.i + a, self.j + b) ].status == self.status:
                                energy -= 15
                            else:
                                energy += 19
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-2, 3):
            for b in range(-2, 3):
                if a in [-2, 2] or b in [-2, 2]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a), (self.j + b))].status == 100:
                                energy -= 35
                            elif cells["{}, {}".format((self.i + a), (self.j + b))].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a), (self.j + b)) ].status == self.status:
                                energy -= 13
                            else:
                                energy += 17
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-3, 4):
            for b in range(-3, 4):
                if a in [-3, 3] or b in [-3, 3]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 30
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 10
                            else:
                                energy += 14
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-4, 5):
            for b in range(-4, 5):
                if a in [-4, 4] or b in [-4, 4]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 25
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 7
                            else:
                                energy += 11
                        else:
                            energy += 0 
                    except:
                        energy += 0
            
        for a in range(-5, 6):
            for b in range(-5, 6):
                if a in [-5, 5] or b in [-5, 5]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 20
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 6
                            else:
                                energy += 10
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-6, 7):
            for b in range(-6, 7):
                if a in [-6, 6] or b in [-6, 6]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 18
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 5
                            else:
                                energy += 9
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-7, 8):
            for b in range(-7, 8):
                if a in [-7, 7] or b in [-7, 7]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 15
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 4
                            else:
                                energy += 8
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-8, 9):
            for b in range(-8, 9):
                if a in [-8, 8] or b in [-8, 8]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 12
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 3
                            else:
                                energy += 7
                        else:
                            energy += 0
                    except:
                        energy += 0

        for a in range(-9, 10):
            for b in range(-9, 10):
                if a in [-9, 9] or b in [-9, 9]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 10
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 2
                            else:
                                energy += 6
                        else: 
                            energy += 0
                    except:
                        energy += 0 

        for a in range(-10, 11):
            for b in range(-10, 11):
                if a in [-10, 10] or b in [-10, 10]:
                    try:
                        if (self.i + a, self.j + b) in self.grid.positions:
                            if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                                energy -= 8
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                                energy += 0
                            elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                                energy -= 1
                            else:
                                energy += 5
                        else:
                            energy += 0
                    except:
                        energy += 0 
    
        return energy