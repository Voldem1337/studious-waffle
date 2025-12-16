
volume = 50

current_resolution_index = 0


music_player = None

def set_volume(new_volume):

    global volume, music_player
    volume = max(0, min(100, new_volume))  #restriction
    if music_player:
        music_player.volume = volume / 100

def set_music_player(player):
    #music player
    global music_player
    music_player = player
    if music_player:
        music_player.volume = volume / 100