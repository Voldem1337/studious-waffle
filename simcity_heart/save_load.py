import json
import time
from pathlib import Path
import logic


def serialize_tile(tile):
    if tile is None:
        return None

    tile_data = {
        'type': tile.__class__.__name__,
        'name': tile.name
    }

    if isinstance(tile, logic.Building):
        tile_data.update({
            'income': tile.income,
            'happiness': tile.happiness,
            'population': tile.population,
            'open_positions': tile.open_positions,
            'build_time': tile.build_time,
            'remaining_time': tile.remaining_time,
            'built': tile.built
        })

    return tile_data


def deserialize_tile(tile_data):
    if tile_data is None:
        return None

    tile_type = tile_data['type']

    if tile_type == 'VerticalRoad':
        return logic.VerticalRoad()
    elif tile_type == 'HorizontalRoad':
        return logic.HorizontalRoad()
    elif tile_type == 'Water':
        return logic.Water()
    elif tile_type == 'Tree':
        return logic.Tree()
    elif tile_type == 'Residential':
        return logic.Residential()
    elif tile_type == 'Commercial':
        return logic.Commercial()
    elif tile_type == 'Industrial':
        return logic.Industrial()
    elif tile_type == 'House':
        house = logic.House()
        house.income = tile_data['income']
        house.happiness = tile_data['happiness']
        house.population = tile_data['population']
        house.open_positions = tile_data['open_positions']
        house.build_time = tile_data['build_time']
        house.remaining_time = tile_data['remaining_time']
        house.built = tile_data['built']
        return house
    elif tile_type == 'Store':
        store = logic.Store()
        store.income = tile_data['income']
        store.happiness = tile_data['happiness']
        store.population = tile_data['population']
        store.open_positions = tile_data['open_positions']
        store.build_time = tile_data['build_time']
        store.remaining_time = tile_data['remaining_time']
        store.built = tile_data['built']
        return store
    elif tile_type == 'Factory':
        factory = logic.Factory()
        factory.income = tile_data['income']
        factory.happiness = tile_data['happiness']
        factory.population = tile_data['population']
        factory.open_positions = tile_data['open_positions']
        factory.build_time = tile_data['build_time']
        factory.remaining_time = tile_data['remaining_time']
        factory.built = tile_data['built']
        return factory
    elif tile_type == 'TownHall':
        townhall = logic.TownHall()
        townhall.income = tile_data['income']
        townhall.happiness = tile_data['happiness']
        townhall.population = tile_data['population']
        townhall.open_positions = tile_data['open_positions']
        townhall.build_time = tile_data['build_time']
        townhall.remaining_time = tile_data['remaining_time']
        townhall.built = tile_data['built']
        return townhall

    return None


def save_game(slot_number=1):
    # Сериализуем grid
    serialized_grid = []
    for row in logic.grid:
        serialized_row = [serialize_tile(tile) for tile in row]
        serialized_grid.append(serialized_row)

    serialized_buildings = []
    for building, x, y in logic.buildings:
        serialized_buildings.append({
            'building': serialize_tile(building),
            'x': x,
            'y': y
        })

    save_data = {
        "city": {
            "money": logic.city_money,
            "happiness": logic.city_happiness,
            "population": logic.city_population,
            "house_count": logic.house_count,
            "store_count": logic.store_count,
            "factory_count": logic.factory_count,
            "city_jobs": logic.city_jobs
        },
        "demand": {
            "residential": logic.residential_demand,
            "commercial": logic.commercial_demand,
            "industrial": logic.industrial_demand
        },
        "grid": serialized_grid,
        "buildings": serialized_buildings,
        "timestamp": time.time()
    }

    save_dir = Path('data')
    save_dir.mkdir(exist_ok=True)

    save_path = save_dir / f'save_{slot_number}.json'
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)

    print(f'Игра сохранена в {save_path}')
    return True


def load_game(slot_number=1):
    save_path = Path('data/worlds') / f'save_{slot_number}.json'

    if not save_path.exists():
        print(f'Файл сохранения {save_path} не найден')
        return False

    with open(save_path, 'r', encoding='utf-8') as f:
        save_data = json.load(f)
    logic.city_money = save_data['city']['money']
    logic.city_happiness = save_data['city']['happiness']
    logic.city_population = save_data['city']['population']
    logic.house_count = save_data['city']['house_count']
    logic.store_count = save_data['city']['store_count']
    logic.factory_count = save_data['city']['factory_count']
    logic.city_jobs = save_data['city']['city_jobs']

    logic.residential_demand = save_data['demand']['residential']
    logic.commercial_demand = save_data['demand']['commercial']
    logic.industrial_demand = save_data['demand']['industrial']

    logic.grid = []
    for row_data in save_data['grid']:
        row = [deserialize_tile(tile_data) for tile_data in row_data]
        logic.grid.append(row)

    logic.buildings = []
    for building_data in save_data['buildings']:
        building = deserialize_tile(building_data['building'])
        x = building_data['x']
        y = building_data['y']
        logic.buildings.append((building, x, y))

    logic.rebuild_buildings_from_grid()

    print(f'Игра загружена из {save_path}')
    return True