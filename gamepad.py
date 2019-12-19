from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event4')
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == keyevent.key_down: 
            if keyevent.keycode == 'BTN_THUMB':
                print("Green")
                print(keyevent.keycode)
            elif keyevent.keycode == 'BTN_THUMB2':
                print("Red")
                print(keyevent.keycode)
            elif keyevent.keycode == 'BTN_TOP':
                print("Yellow")
                print(keyevent.keycode)
            elif keyevent.keycode[0] == 'BTN_JOYSTICK':
                print("Blue")
                print(keyevent.keycode)
            else:
                print(keyevent.keycode)
        
