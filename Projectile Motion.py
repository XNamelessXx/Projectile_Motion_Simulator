import math
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation

#Constants
g = 9.81 
radians_to_degrees = 180 / math.pi

#Functions

#Without Drag
def horizontal_initial_velocity_func(initial_velocity, launch_angle):
    return initial_velocity * math.cos(launch_angle)

def vertical_initial_velocity_func(initial_velocity, launch_angle):
    return initial_velocity * math.sin(launch_angle)

def horizontal_displacement_func(horizontal_initial_velocity, time):
    return horizontal_initial_velocity * time

def vertical_displacement_func(vertical_initial_velocity, time):
    return vertical_initial_velocity * time + 0.5 * -g * (time ** 2)

#With Drag
def drag_func(velocity,radius):
    return -0.5 * 1.225 * velocity * abs(velocity) * 0.5 * math.pi * (radius ** 2)

def vertical_acceleration_func(mass, drag_force_vertical):
    weight = -mass * g
    return (weight + drag_force_vertical) / mass

def horizontal_acceleration_func(drag_force_horizontal, mass):
    return drag_force_horizontal / mass

def vertical_velocity_changed(vertical_velocity, vertical_acceleration, dt):
    return vertical_velocity + vertical_acceleration * dt

def horizontal_velocity_changed(horizontal_velocity, horizontal_acceleration, dt):
    return horizontal_velocity + horizontal_acceleration * dt

def horizontal_displacement_with_drag_func(horizontal_displacement_with_drag, horizontal_velocity, dt):
    return horizontal_displacement_with_drag + horizontal_velocity * dt

def vertical_displacement_with_drag_func(vertical_displacement_with_drag, vertical_velocity, dt):
    return vertical_displacement_with_drag + vertical_velocity * dt

#Input
def correct_input(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number <= 0:
                print("Please enter a positive number.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a number.")

initial_velocity = correct_input("Enter initial velocity (m/s): ")
while True: 
    question = input("Is the launch angle in degrees or radians? (d/r): ")
    if question == "d":
        launch_angle = math.radians(correct_input("Enter launch angle in degrees: "))
        break
    elif question == "r":
        launch_angle = float(correct_input("Enter launch angle in radians: "))
        break
    else:
        print("Invalid input. Please enter 'd' for degrees or 'r' for radians.")

mass = correct_input("Enter mass of the projectile (kg): ")
radius = correct_input("Enter radius of the projectile (m): ")

#Without Drag Program
time = 0
horizontal_displacement = 0
vertical_displacement = 0

horizontal_initial_velocity = horizontal_initial_velocity_func(initial_velocity, launch_angle)
vertical_initial_velocity = vertical_initial_velocity_func(initial_velocity, launch_angle)


dt = ((2 * vertical_initial_velocity) / g) / 2000

horizontal_displacements = [0]
vertical_displacements = [0]

while vertical_displacement >= 0:
    time += dt
    horizontal_displacement = horizontal_displacement_func(horizontal_initial_velocity, time)
    vertical_displacement = vertical_displacement_func(vertical_initial_velocity, time)

    horizontal_displacements.append(horizontal_displacement)
    vertical_displacements.append(vertical_displacement)

flight_time_without_drag = time

#With Drag
time = 0
horizontal_velocity = horizontal_initial_velocity
vertical_velocity = vertical_initial_velocity

horizontal_displacement_with_drag = 0
vertical_displacement_with_drag = 0

horizontal_displacements_with_drag = [0]
vertical_displacements_with_drag = [0]

while vertical_displacement_with_drag >= 0:
    time += dt
    drag_force_horizontal = drag_func(horizontal_velocity, radius)
    drag_force_vertical = drag_func(vertical_velocity, radius)
    horizontal_acceleration = horizontal_acceleration_func(drag_force_horizontal, mass)
    vertical_acceleration = vertical_acceleration_func(mass, drag_force_vertical)

    horizontal_velocity = horizontal_velocity_changed(horizontal_velocity, horizontal_acceleration, dt)
    vertical_velocity = vertical_velocity_changed(vertical_velocity, vertical_acceleration, dt)

    horizontal_displacement_with_drag = horizontal_displacement_with_drag_func(horizontal_displacement_with_drag, horizontal_velocity, dt)
    vertical_displacement_with_drag = vertical_displacement_with_drag_func(vertical_displacement_with_drag, vertical_velocity, dt)

    horizontal_displacements_with_drag.append(horizontal_displacement_with_drag)
    vertical_displacements_with_drag.append(vertical_displacement_with_drag)

flight_time_with_drag = time

#Plotting Graph
fig, ax = plot.subplots()
ax.set_aspect('equal', adjustable = 'box')

ax.set_ylabel("Vertical Displacement (m)")
ax.set_xlabel("Horizontal Displacement (m)")

padding_y = max(vertical_displacements)* 0.2
padding_x = max(horizontal_displacements)* 0.1

ax.set_ylim(0 - padding_y, max(vertical_displacements) + padding_y)
ax.set_xlim(0 - padding_x, max(horizontal_displacements) + padding_x)

animated_plot, = ax.plot([], [], label = 'Without Drag')
animated_plot_for_drag, = ax.plot([], [], label = 'With Drag')

def update(frame):
        animated_plot.set_data(horizontal_displacements[:frame], vertical_displacements[:frame])
        animated_plot_for_drag.set_data(horizontal_displacements_with_drag[:frame], vertical_displacements_with_drag[:frame])
        return animated_plot, animated_plot_for_drag,

max_y_without_drag = max(vertical_displacements)
max_y_without_drag_index = vertical_displacements.index(max_y_without_drag)
max_x_without_drag = horizontal_displacements[max_y_without_drag_index]

max_y_with_drag = max(vertical_displacements_with_drag)
max_y_with_drag_index = vertical_displacements_with_drag.index(max_y_with_drag)
max_x_with_drag = horizontal_displacements_with_drag[max_y_with_drag_index]

animation = FuncAnimation(fig, update, frames=len(horizontal_displacements), interval=1, repeat=False, blit=True)

plot.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.65), ncols = 2)
ax.text(0.5, -1.5, f'Max Height (No Drag): {max_y_without_drag:.2g} m    Max Height (With Drag): {max_y_with_drag:.2g} m'
        f'\n Flight Time (No Drag): {flight_time_without_drag:.2g} s    Flight Time (With Drag): {flight_time_with_drag:.2g} s', ha='center', va='top', transform=ax.transAxes)

plot.grid()
plot.show()

