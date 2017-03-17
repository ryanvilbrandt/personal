# http://cyber-omelette.blogspot.ca/2016/11/python-n-body-orbital-simulation.html

import math
import matplotlib.pyplot as plot
# from mpl_toolkits.mplot3d import Axes3D

G = 6.67408e-11  # m3 kg-1 s-2

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Velocity:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Acceleration:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Body:
    def __init__(self, p: Point, m: float, v: Velocity, name: str=""):
        """
        :param p: 3D point
        :param m: float
        :param v: 3D vector
        :param name:
        :return:
        """
        self.location = p
        self.mass = m
        self.velocity = v
        self.name = name

def calculate_single_body_acceleration(bodies: list, body_index: int) -> Acceleration:
    acceleration = Acceleration(0, 0, 0)
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body.location.x - external_body.location.x)**2 + \
                (target_body.location.y - external_body.location.y)**2 + \
                (target_body.location.z - external_body.location.z)**2
            r = math.sqrt(r)
            tmp = G * external_body.mass / r**3
            acceleration.x += tmp * (external_body.location.x - target_body.location.x)
            acceleration.y += tmp * (external_body.location.y - target_body.location.y)
            acceleration.z += tmp * (external_body.location.z - target_body.location.z)
    return acceleration

def compute_velocity(bodies: list, time_step: int=1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)
        target_body.velocity.x += acceleration.x * time_step
        target_body.velocity.y += acceleration.y * time_step
        target_body.velocity.z += acceleration.z * time_step

def update_location(bodies: list, time_step: int=1):
    for target_body in bodies:
        target_body.location.x += target_body.velocity.x * time_step
        target_body.location.y += target_body.velocity.y * time_step
        target_body.location.z += target_body.velocity.z * time_step

def compute_gravity_step(bodies: list, time_step: int=1):
    compute_velocity(bodies, time_step=time_step)
    update_location(bodies, time_step=time_step)

def run_simulation(bodies: list, time_step: int=1, number_of_steps: int=10000, report_freq: int=100) -> list:
    #create output container for each body
    body_locations_hist = []
    for current_body in bodies:
        body_locations_hist.append({"x": [], "y": [], "z": [], "name": current_body.name})

    for i in range(1, number_of_steps):
        compute_gravity_step(bodies, time_step=time_step)

        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index].location.x)
                body_location["y"].append(bodies[index].location.y)
                body_location["z"].append(bodies[index].location.z)

    return body_locations_hist

def plot_output(bodies, outfile=None):
    fig = plot.figure()
    colours = ['r','b','g','y','m','c']
    ax = fig.add_subplot(1,1,1, projection='3d')
    max_range = 0
    for current_body in bodies:
        max_dim = max(max(current_body["x"]),max(current_body["y"]),max(current_body["z"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_body["x"], current_body["y"], current_body["z"], c = random.choice(colours), label = current_body["name"])

    ax.set_xlim([-max_range,max_range])
    ax.set_ylim([-max_range,max_range])
    ax.set_zlim([-max_range,max_range])
    ax.legend()

    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()

if __name__ == "__main__":

    #planet data (location (m), mass (kg), velocity (m/s)
    sun = {"location": Point(0, 0, 0), "mass": 2e30, "velocity": Velocity(0, 0, 0)}
    mercury = {"location": Point(0, 5.7e10, 0), "mass": 3.285e23, "velocity": Velocity(47000, 0, 0)}
    venus = {"location": Point(0, 1.1e11, 0), "mass": 4.8e24, "velocity": Velocity(35000, 0, 0)}
    earth = {"location": Point(0, 1.5e11, 0), "mass": 6e24, "velocity": Velocity(30000, 0, 0)}
    mars = {"location": Point(0, 2.2e11, 0), "mass": 2.4e24, "velocity": Velocity(24000, 0, 0)}
    jupiter = {"location": Point(0, 7.7e11, 0), "mass": 1e28, "velocity": Velocity(13000, 0, 0)}
    saturn = {"location": Point(0, 1.4e12, 0), "mass": 5.7e26, "velocity": Velocity(9000, 0, 0)}
    uranus = {"location": Point(0, 2.8e12, 0), "mass": 8.7e25, "velocity": Velocity(6835, 0, 0)}
    neptune = {"location": Point(0, 4.5e12, 0), "mass": 1e26, "velocity": Velocity(5477, 0, 0)}
    pluto = {"location": Point(0, 3.7e12, 0), "mass": 1.3e22, "velocity": Velocity(4748, 0, 0)}

    #build list of planets in the simulation, or create your own
    bodies = [
        Body(sun["location"], sun["mass"], sun["velocity"], name="sun"),
        Body(earth["location"], earth["mass"], earth["velocity"], name="earth"),
        Body(mars["location"], mars["mass"], mars["velocity"], name="mars"),
        Body(venus["location"], venus["mass"], venus["velocity"], name="venus"),
    ]

    motions = run_simulation(bodies, time_step=100, number_of_steps=100000, report_freq=10000)
    plot_output(motions)
