import random

def get_streamer_data(name, current_viewers):

    change = random.randint(-500, 500)
    
    viewers = current_viewers + change

    if viewers < 0:
        viewers = 0

    return {
        "name": name, 
        "viewers": viewers
    }