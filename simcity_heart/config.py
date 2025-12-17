import json
from pathlib import Path

volume = 50

current_resolution_index = 0

music_player = None

current_world_name = "My World"


def set_volume(new_volume):
    global volume, music_player
    volume = max(0, min(100, new_volume))
    if music_player:
        music_player.volume = volume / 100
    volume = new_volume
    save_config()


def set_music_player(player):
    global music_player
    music_player = player
    if music_player:
        music_player.volume = volume / 100



def get_save_filename():
    safe_name = current_world_name.replace(' ', '_').lower()
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ['_', '-'])
    return f"save_{safe_name}.json"


CONFIG_PATH = Path("../simcity_heart/data/config.json")

def save_config():

    data = {
        "volume": volume,
        "current_resolution_index": current_resolution_index
    }
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_config():
    global volume, current_resolution_index

    if not CONFIG_PATH.exists():
        return  

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    volume = data.get("volume", volume)
    current_resolution_index = data.get(
        "current_resolution_index",
        current_resolution_index
    )
