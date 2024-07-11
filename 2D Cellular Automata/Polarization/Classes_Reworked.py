import math

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
        self.nucleus = False
        self.polarity_protein = False
        self.color = "white"
        self.group = ""
        self.grid = ""

    def get_energy(self, positions, cells, distance_scaler):
        energy = 0
        for pos in positions:

            if pos != (self.i, self.j) and pos in self.grid.positions:
                x, y = pos
                other = cells["{}, {}".format(x, y)]

                distance = math.sqrt((x - self.i)**2 + (y - self.j)**2)
                strength = 1/distance * distance_scaler

                if self.status == 1:
                    if other.status == 1:
                        rate = -20
                    elif other.status == 2:
                        rate = 20
                    else:
                        rate = 0

                elif self.status == 2:
                    if other.status == 1:
                        rate = 20
                    elif other.status == 2:
                        rate = -20
                    else:
                        rate = 0

                else:
                    rate = 0

                energy += strength * rate
            
        return energy