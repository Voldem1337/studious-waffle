import random



# STARTING DATA
city_money = 10000
city_happiness = 0
city_population = 0
house_count = 0
store_count = 0
factory_count = 0
city_jobs = 0

buildings = []

residential_demand = 0
commercial_demand = 0
industrial_demand = 0





# THE GRID
grid = [[None for _ in range(10)] for _ in range(10)]

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
    for x in range(4, 6):
        grid[y][x] = VerticalRoad()

grid[7][9] = Water()
grid[7][8] = Water()
grid[7][7] = Water()
grid[6][9] = Water()
grid[6][8] = Water()
grid[6][7] = Water()
grid[5][9] = Water()
grid[5][8] = Water()
grid[5][7] = Water()

grid[1][0] = Tree()
grid[2][1] = Tree()
grid[7][2] = Tree()
grid[1][8] = Tree()
grid[8][8] = Tree()
grid[8][9] = Tree()


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
        self.build_time = 1 # 10 seconds to build
        self.remaining_time = self.build_time
        self.built = False

class Store(Building):
    def __init__(self):
        super().__init__('Store', income=random.randint(12, 18), happiness=0.05, open_positions=random.randint(3, 10))
        self.build_time = 3  # 15 seconds to build
        self.remaining_time = self.build_time
        self.built = False

class Factory(Building):
    def __init__(self):
        super().__init__('Factory', income=random.randint(25, 35), happiness=0.0, open_positions=random.randint(8, 20))
        self.build_time = 5  # 30 seconds to build
        self.remaining_time = self.build_time
        self.built = False


# The process of buying and placing a building
def try_placing_zone(x, y, zone_type):
    print(f"TRY placing a zone at {x}, {y}")
    zone = zone_type()

    if grid[y][x] is None:
        print(f"✅ Conditions met — placing a {zone.name}")
        grid[y][x] = zone
        return True
    print(f"❌ Conditions failed — grid[{x},{y}]={grid[y][x]}")
    return False
'''
def try_building_in_zone(x, y):
    global house_count, store_count, factory_count,\
        city_population, city_jobs

    build = False

    # if tile is Residential Zone
    if isinstance(grid[y][x], Residential):
        house = House()

        if house_count < 5:
            build = True

        # if at least half of city population is employed
        elif employed_population * 2 >= city_population:
            build = True

        if build:
            # Place a House in the Residential zone
            place_building(x, y, house)
            house_count += 1
            # Houses give population
            city_population += house.population
            unemployed_population += house.population

    # if tile is Commercial Zone
    elif isinstance(grid[y][x], Commercial):
        store = Store()
        if store_count < 3:
            build = True
        # if less than third of city is employed
        elif employed_population * 3 < city_population:
            build = True

        if build:
            place_building(x, y, store)
            store_count += 1
            city_open_job_positions += store.open_positions
            if unemployed_population >= city_open_job_positions:
                city_open_job_positions = 0
                unemployed_population -= city_open_job_positions
            else:
                unemployed_population = 0
                city_open_job_positions -= unemployed_population


    # if tile is Industrial Zone
    elif isinstance(grid[y][x], Industrial):
        factory = Factory()
        if factory_count < 2:
            build = True
        # if less than half of city is employed
        elif employed_population * 2 < city_population:
            build = True

        if build:
            place_building(x, y, factory)
            factory_count += 1
            city_jobs += factory.open_positions

            if unemployed_population >= city_open_job_positions:
                city_open_job_positions = 0
                unemployed_population -= city_open_job_positions
            else:
                unemployed_population = 0
                city_open_job_positions -= unemployed_population

    employed_population = city_population - unemployed_population
'''
def try_building_in_zone(x, y):
    zone = grid[y][x]
    build = False

    # --- RESIDENTIAL ---
    if isinstance(zone, Residential):
        # allow early growth OR demand-based growth
        if house_count < 6 or residential_demand > 0:
            build = True

        if build:
            house = House()
            place_building(x, y, house)
            # DO NOT add population here anymore
            # DO NOT increase happiness here
            # construction system will handle it
            return

    # --- COMMERCIAL ---
    if isinstance(zone, Commercial):
        if commercial_demand > 0:
            build = True

        if build:
            store = Store()
            place_building(x, y, store)
            # DO NOT add jobs here
            return

    # --- INDUSTRIAL ---
    if isinstance(zone, Industrial):
        if industrial_demand > 0:
            build = True

        if build:
            factory = Factory()
            place_building(x, y, factory)
            # DO NOT add jobs here
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

    for building, x, y in buildings:
        if not building.built:
            building.remaining_time -= delta_time

            if building.remaining_time <= 0:
                building.built = True
                city_population += building.population
                city_jobs += building.open_positions


# RESOURCES AND TIME UPDATES
# We will be running it through on_update() function every second.
# (So the Buildings will bring income and happiness every second)
def update_city():
    global city_money, city_happiness, city_population


    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Calculating demand for the try_building_in_zone to work properly
            calculate_demand()
            # Building a building if the demand is higher than 0
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