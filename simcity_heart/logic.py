from constants import city_happiness, city_money

# LOGIC COMPONENTS:

# THE GRID
grid = [[None for _ in range(10)] for _ in range(10)]

def get_tile(x, y):
    return grid[y][x]

def place_building(x, y, building):
    if grid[y][x] is None:
        grid[x][y] = building

# Checking if it works
for row in grid:
    print(row)


# BUILDINGS AND THEIR EFFECTS
class Building:
    def __init__(self, name, cost, income=0, happiness=0):
        self.name = name
        self.cost = cost
        self.income = income
        self.happiness = happiness

# House characteristics
class House(Building):
    def __init__(self):
        super().__init__('House', cost=1000, happiness=1)

# Factory characteristics
class Factory(Building):
    def __init__(self):
        super().__init__('Factory', cost=3000, income=50, happiness=-2)




# The process of buying and placing a building
def try_placing_building(x, y, building_type):
    global city_money, city_happiness
    building = building_type()
    if grid[y][x] is None and city_money >= building.cost:
        grid[y][x] = building
        city_money -= building.cost

# RESOURCES AND TIME UPDATES
# We will be running it through on_update() function every second.
# (So the Buildings will bring income and happiness every second)
def update_city():
    global city_money, city_happiness
    for row in grid:
        for tile in row:
            # If some building is placed on this tile,
            if tile is not None:
                # then it gives income and happiness
                city_money += tile.income
                city_happiness += tile.happiness

#GAME STATE MANAGEMENT
game_state = ''


# Testing
print(city_money)
try_placing_building(3, 3, Factory)
try_placing_building(3, 4, House)
print(city_money)
print(city_happiness)
update_city()
print(city_money)
print(city_happiness)
for row in grid:
    print(row)