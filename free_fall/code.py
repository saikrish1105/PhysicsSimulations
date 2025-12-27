import math

# variables
g = 9.8
initial_height = 100

# time to reach ground
time_to_reach = math.sqrt(2*initial_height/g)
print("Time to hit ground = ",time_to_reach)

# velocity when it hits ground
velocity_ground = math.sqrt(2*g*initial_height)
print("velocity when it hits ground = ",velocity_ground)

# height reached after first bounce
e = 0.8 # coefficient of restitution
velocity_after_bounce = e * velocity_ground
max_height = (velocity_after_bounce**2)/(2*(g))
print("Max height after bounce = ",max_height)

# lets calculate for multiple bounces until it touches the floor
while max_height > 0.1:
    velocity_after_bounce = e*math.sqrt(2*g*max_height)
    max_height = (velocity_after_bounce**2)/(2*(g))
    print("Height after bounce = ",max_height,"\n")

# v = u + at
# s = ut + 1/2 at^2
# v2 - u2 = 2as
# v2 = 2gs 