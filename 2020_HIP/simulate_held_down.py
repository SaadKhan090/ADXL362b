import keyboard
import time

# Sends 20 "key down" events in 0.1 second intervals, followed by a single
# "key up" event.

time.sleep(7)
print("done")
for i in range(20):
    keyboard.send('left arrow')
    time.sleep(0.1)

