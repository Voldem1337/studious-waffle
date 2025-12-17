import random

# STARTING DATA
city_money = 10000
city_happiness = 0
city_population = 0
city_jobs = 0

buildings = []
house_count = 0
store_count = 0
factory_count = 0

residential_demand = 0
commercial_demand = 0
industrial_demand = 0





# THE GRID
grid = [[None for _ in range(36)] for _ in range(22)]

# Since the y coordinates are measured from the top in matrix, the matrix maps y is reversed compared to
# the actual game map.


#Basic functions
def get_tile(x, y):
    return grid[y][x]

def place_building(x, y, building):
    grid[y][x] = building
    print(f'{building} BUILT on {x}, {y}')
    buildings.append((building, x, y))


# Creating Placeable objects (object that can be placed by a player)
class Placeable:
    def __init__(self, name, income=0, happiness=0.0, population=0):
        self.name = name
        self.income = income
        self.happiness = happiness
        self.population = population


#ROADS
class VerticalRoad(Placeable):
    def __init__(self):
        super().__init__('Vertical Road')

class HorizontalRoad(Placeable):
    def __init__(self):
        super().__init__('Horizontal Road')

#WATER
class Water(Placeable):
    def __init__(self):
        super().__init__('Water')

#TREES
class Tree(Placeable):
    def __init__(self):
        super().__init__('Tree')

#Drawing the starting location
for y in range(len(grid)):
    for x in range(17, 19):
        grid[y][x] = VerticalRoad()

grid[16][22] = Water()
grid[16][21] = Water()
grid[16][20] = Water()
grid[15][22] = Water()
grid[15][21] = Water()
grid[15][20] = Water()
grid[14][22] = Water()
grid[14][21] = Water()
grid[14][20] = Water()

grid[10][13] = Tree()
grid[11][14] = Tree()
grid[16][15] = Tree()
grid[10][21] = Tree()
grid[17][21] = Tree()
grid[17][22] = Tree()




for row in grid:
    print(row)


# ZONES AND THEIR EFFECTS
class Zone(Placeable):
    def __init__(self, name):
        super().__init__(name)

# House characteristics
class Residential(Zone):
    def __init__(self):
        super().__init__('Residential Zone')

class Commercial(Zone):
    def __init__(self):
        super().__init__('Commercial Zone')

# FactoryZone characteristics
class Industrial(Zone):
    def __init__(self):
        super().__init__('Industrial Zone')

# Buildings (can't be place by a player)
class Building:
    def __init__(self, name, income=0, happiness=0.0, population=0, open_positions=0):
        self.name = name
        self.income = income
        self.happiness = happiness
        self.population = population
        self.open_positions = open_positions

        self.build_time = 0
        self.remaining_time = 0
        self.built = True

# Zone Buildings
class House(Building):
    def __init__(self):
        super().__init__('House', 0, happiness=0.01, population=random.randint(7, 10))

        # Building takes time
        self.build_time = 10 # 10 seconds to build
        self.remaining_time = self.build_time
        self.built = False

class Store(Building):
    def __init__(self):
        super().__init__('Store', income=random.randint(12, 18), happiness=0.05, open_positions=random.randint(3, 10))
        self.build_time = 15  # 15 seconds to build
        self.remaining_time = self.build_time
        self.built = False

class Factory(Building):
    def __init__(self):
        super().__init__('Factory', income=random.randint(25, 35), happiness=0.0, open_positions=random.randint(8, 20))
        self.build_time = 20  # 20 seconds to build
        self.remaining_time = self.build_time
        self.built = False


# The process of placing a placeable
def try_placing_placeable(x, y, placeable):
    print(f"TRY placing a zone at {x}, {y}")
    placeable = placeable()

    if grid[y][x] is None:
        print(f"✅ Conditions met — placing a {placeable.name}")
        grid[y][x] = placeable
        return True
    print(f"❌ Conditions failed — grid[{x},{y}]={grid[y][x]}")
    return False


def try_building_in_zone(x, y):
    global construction_started_this_tick
    zone = grid[y][x]
    build = False

    # --- RESIDENTIAL ---
    if isinstance(zone, Residential):
        # allow early growth OR demand-based growth
        if house_count < 6 or residential_demand > 0.1:
            build = True

        if build:
            house = House()
            place_building(x, y, house)
            construction_started_this_tick = True
            return

    # --- COMMERCIAL ---
    if isinstance(zone, Commercial):
        if commercial_demand > 0:
            build = True

        if build:
            store = Store()
            place_building(x, y, store)
            construction_started_this_tick = True
            return

    # --- INDUSTRIAL ---
    if isinstance(zone, Industrial):
        if industrial_demand > 0:
            build = True

        if build:
            factory = Factory()
            place_building(x, y, factory)
            construction_started_this_tick = True
            return



def calculate_demand():
    global residential_demand, commercial_demand, industrial_demand

    happiness_factor = city_happiness / 100 # scaling happiness to 0-1


    employed_population = min(city_population, city_jobs)
    unemployed_population = city_population - employed_population

    residential_demand = (
            (city_jobs - employed_population) - (unemployed_population * 1) + (happiness_factor * 5)
    )

    if city_population > 10:
        commercial_demand = (
            employed_population * 0.4 -
            store_count * 5 +
            city_population * 0.1
        )
    else:
        commercial_demand = 0

    if city_population > 15:
        industrial_demand = (
            unemployed_population * 1 +
            city_population * 0.15 +
            store_count * 0.6 -
            factory_count * 3
        )
    else:
        industrial_demand = 0

def update_construction(delta_time):
    global city_population, city_jobs

    finished = []

    for building, x, y in buildings:
        if not building.built:
            building.remaining_time -= delta_time

            if building.remaining_time <= 0:
                building.built = True
                city_population += building.population
                city_jobs += building.open_positions
                finished.append((building, x, y))

    return finished



# RESOURCES AND TIME UPDATES
# We will be running it through on_update() function every second.
# (So the Buildings will bring income and happiness every second)
def update_city():
    global city_money, city_happiness, city_population, store_count, house_count, factory_count, construction_started_this_tick

    store_count = sum(isinstance(b, Store) for b, _, _ in buildings)
    house_count = sum(isinstance(b, House) for b, _, _ in buildings)
    factory_count = sum(isinstance(b, Factory) for b, _, _ in buildings)

    construction_started_this_tick = False



    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Calculating demand for the try_building_in_zone to work properly
            calculate_demand()
            # Building a building if the demand is higher than 0
            if not construction_started_this_tick:
                try_building_in_zone(x, y)

    for row in grid:
        for tile in row:
            # If something is placed on this tile,
            if tile is not None:
                # then it gives income
                city_money += tile.income

                # and happiness
                if city_happiness + tile.happiness > 100:
                    city_happiness = 100
                elif city_happiness + tile.happiness <= 0:
                    city_happiness = 0
                else:
                    city_happiness += tile.happiness



#GAME STATE MANAGEMENT
game_state = ''

'''
#Testing
#for row in grid:
 #   print(row)


print('-------------------------------------------')
try_placing_zone(0, 0, Industrial)
try_placing_zone(3, 4, Residential)
try_placing_zone(9, 2, Residential)
try_placing_zone(9, 3, Commercial)
update_city()
update_city()
update_city()

print(f'Factories: {factory_count}, Employed population: {calculate_demand()}, Houses: {house_count}, Stores: {store_count}, City population: {city_population}')

#print(city_money)
#for row in grid:
 #   print(row)

'''