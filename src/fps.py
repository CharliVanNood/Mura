import time
from  src.utils.font import comic_sans

last_time = time.time()
time_delta = 1
update_interval = 0.5  # Update FPS display every 0.5 seconds
last_update_time = time.time()
current_fps = 0


# returns the fps on the current frame
def get_fps():
    global last_time
    global time_delta
    global last_update_time
    global current_fps

    new_time = time.time()
    time_delta = new_time - last_time
    deltatime = 60 / (1 / time_delta)
    if deltatime > 10: deltatime = 10
    last_time = new_time

    if time_delta == 0: time_delta = 0.001

    if new_time - last_update_time >= update_interval: # Makes sure it only updates every 0.5 seconds
        current_fps = round(1 / time_delta,1)
        if current_fps >= 5:
            current_fps = int(current_fps)
        last_update_time = new_time

    return (current_fps, deltatime)


# returns a surface with the fps on it
def render_fps(fps):
    return comic_sans.render(f"FPS: {fps}", False, (255, 0, 0))

def get_time_delta():
    return time_delta