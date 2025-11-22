from constants import city_happiness, city_money

# LOGIC COMPONENTS:

# THE GRID
grid = [[None for _ in range(10)] for _ in range(10)]

#ROADS
class Road:
    def __init__(self, name, income=0, happiness=0.0):
        self.name = name
        self.income = income
        self.happiness = happiness

class BigRoad(Road):
    def __init__(self):
        super().__init__('Big Road')

#WATER
class Water:
    def __init__(self, name='Water', income=0, happiness=0.0):
        self.name = name
        self.income = income
        self.happiness = happiness

#Drawing the starting location
for y in range(len(grid)):
    for x in range(4, 6):
        grid[y][x] = BigRoad()

#grid[7][9] = Water()
#grid[7][8] = Water()
#grid[7][7] = Water()
#grid[6][9] = Water()
#grid[6][8] = Water()
#grid[6][7] = Water()
grid[7][9] = Water()
grid[7][8] = Water()
grid[7][7] = Water()
grid[6][9] = Water()
grid[6][8] = Water()
grid[6][7] = Water()
grid[5][9] = Water()
grid[5][8] = Water()
grid[5][7] = Water()

# Reversing the grid so that the y coordinate would be measured from the bottom. (Since it's matrix the y coordinates were measured from the top before)
grid.reverse()


#for row in grid:
 #   print(row)




def get_tile(x, y):
    return grid[y][x]

def place_building(x, y, building):
    if grid[y][x] is None:
        grid[y][x] = building


# BUILDINGS AND THEIR EFFECTS
class Zone:
    def __init__(self, name, income=0, happiness=0.0):
        self.name = name
        self.income = income
        self.happiness = happiness

# House characteristics
class House(Zone):
    def __init__(self):
        super().__init__('House', happiness=0.1)

class Store(Zone):
    def __init__(self):
        super().__init__('Store', income=15, happiness=0.1)

# Factory characteristics
class Factory(Zone):
    def __init__(self):
        super().__init__('Factory', income=30, happiness=-0.2)




# The process of buying and placing a building
def try_placing_zone(x, y, zone_type):
    global city_money, city_happiness
    print(f"TRY placing a zone at {x}, {y}")
    zone = zone_type()

    if grid[y][x] is None:
        print("✅ Conditions met — placing a zone")
        grid[y][x] = zone
        return True
    print(f"❌ Conditions failed — grid[{x},{y}]={grid[y][x]}")
    return False

# RESOURCES AND TIME UPDATES
# We will be running it through on_update() function every second.
# (So the Buildings will bring income and happiness every second)
def update_city():
    global city_money, city_happiness
    for row in grid:
        for tile in row:
            # If something is placed on this tile,
            if tile is not None:
                # then it gives income and happiness
                city_money += tile.income
                if city_happiness + tile.happiness > 100:
                    city_happiness = 100
                elif city_happiness + tile.happiness <= 0:
                    city_happiness = 0
                else:
                    city_happiness += tile.happiness

#GAME STATE MANAGEMENT
game_state = ''


#Testing
for row in grid:
    print(row)
print('-------------------------------------------')
#try_placing_zone(3, 3, Factory)
#try_placing_zone(3, 4, House)
#try_placing_zone(9, 2, House)
#update_city()
for row in grid:
    print(row)