import arcade
from pathlib import Path

saves_dir = Path('data/worlds')

for file in saves_dir.iterdir():
    print(file)