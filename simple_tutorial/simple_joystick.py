import pygame, time

# --- Initialize ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()

print(f"🎮 Joystick: {joy.get_name()}")
print(f"  Axes: {joy.get_numaxes()}")
print(f"  Buttons: {joy.get_numbuttons()}")
print(f"  Hats: {joy.get_numhats()}")
print("\nMove or press anything on your joystick to see changes...\n")

# --- Store previous states ---
prev_axes = [0.0] * joy.get_numaxes()
prev_buttons = [0] * joy.get_numbuttons()
prev_hats = [(0, 0)] * joy.get_numhats()

try:
    while True:
        pygame.event.pump()

        # --- Read current states ---
        axes = [round(joy.get_axis(i), 2) for i in range(joy.get_numaxes())]
        buttons = [joy.get_button(i) for i in range(joy.get_numbuttons())]
        hats = [joy.get_hat(i) for i in range(joy.get_numhats())]

        # --- Check for axis changes ---
        for i, (prev, curr) in enumerate(zip(prev_axes, axes)):
            if abs(curr - prev) > 0.05:  # threshold to avoid noise
                print(f"🕹️ Axis {i} changed: {curr} (range: -1.0 to 1.0)")
                prev_axes[i] = curr

        # --- Check for button changes ---
        for i, (prev, curr) in enumerate(zip(prev_buttons, buttons)):
            if curr != prev:
                state = "Pressed" if curr else "Released"
                print(f"🔘 Button {i} {state}")
                prev_buttons[i] = curr

        # --- Check for hat (D-pad) changes ---
        for i, (prev, curr) in enumerate(zip(prev_hats, hats)):
            if curr != prev:
                print(f"🎯 Hat {i} changed: {curr} (x,y) → up={curr[1]==1}, down={curr[1]==-1}, left={curr[0]==-1}, right={curr[0]==1}")
                prev_hats[i] = curr

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    pygame.quit()
