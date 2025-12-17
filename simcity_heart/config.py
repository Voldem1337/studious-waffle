volume = 50

current_resolution_index = 0

music_player = None

def set_volume(new_volume):
    global volume, music_player
    if music_player:
        music_player.volume = volume / 100

def set_music_player(player):
    global music_player
    music_player = player
    if music_player:
        music_player.volume = volume / 100