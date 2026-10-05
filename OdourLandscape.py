import numpy as np
import matplotlib.pyplot as plt
#odour landscape
def odour_concentration(x, y, source_x=10, source_y=0):
    """
    Smooth odour concentration field.
    The source is at postion (source_x, source_y).
    Concentration decreases with distance.
    """

    distance = np.sqrt( (x - source_x)**2 +(y - source_y)**2)

    # characteristic length scale of the odour
    decay_length = 8.0

    concentration = np.exp(-distance / decay_length)

    return concentration


#parameters for simulation

dt = 0.5                 # timestep (seconds)
speed = 0.22             # worm speed (mm/s)
step_size = speed * dt   # distance travelled per timestep

n_steps = 2000           # 1000 seconds
n_worms = 100

# correlated curvature parameters from Yoshida et al. paper
curvature_memory = 0.933
curvature_noise = 11.6

#pirouette paramers
#simplified values for reconstruction, paper's exact behavioural parameters are presented graphically (rather than as a complete numerical table)

base_pirouette_prob = 0.025

# positive value means: moving down the attractive gradient increases turning
pirouette_index = 0.025


#weathervane parameters
# controls strength of klinotaxis.
weathervane_index = 8.0

# additional functions
def angle_difference(a, b):
    # smallest difference between two angles.
    return np.arctan2( np.sin(a - b),np.cos(a - b))


def source_bearing(x, y, direction, source_x=10, source_y=0):
    """
    Calculate angle of the odour source relative
    to the worm's current direction.

    theta = 0: source directly ahead
    theta > 0: source to one side
    theta < 0:source to the other side
    """

    angle_to_source = np.arctan2(source_y - y,source_x - x)
    theta = angle_difference(angle_to_source, direction )
    return theta


def pirouette_probability(theta):
    """
    Simplified Yoshida-style klinokinesis model.

    cos(theta) represents the component of the
    source direction along the worm's direction
    of travel.

    Moving towards the source:
        cos(theta) > 0
        lower probability of pirouette

    Moving away:
        cos(theta) < 0
        higher probability of pirouette
    """

    probability = ( base_pirouette_prob- pirouette_index * np.cos(theta) )

    return np.clip(probability, 0, 1)

#simulate one worm
def simulate_worm( mechanism="both", start_x=0,start_y=0,start_direction=0,source_x=10, source_y=0):
    """
    Simulate one worm.

    mechanism can be:

        "random"
        "klinokinesis"
        "klinotaxis"
        "both"
    """

    x = start_x
    y = start_y
    direction = start_direction

    curvature = 0.0

    trajectory_x = np.zeros(n_steps)
    trajectory_y = np.zeros(n_steps)

    concentrations = np.zeros(n_steps)

    pirouettes = 0

    for i in range(n_steps):
        #records current position
        trajectory_x[i] = x
        trajectory_y[i] = y

        concentrations[i] = odour_concentration( x, ysource_x, source_y)
        # correlated random curvature
        random_noise = np.random.normal(0, curvature_noise)
        curvature = ( curvature_memory * curvature + random_noise )
        # Angle between worm direction and source
        theta = source_bearing(x, y, direction, source_x, source_y)

        # Klinotaxis / Weathervane

        if mechanism in ["klinotaxis", "both"]:

            # Yoshida: psi = phi + alpha sin(theta)

            turning_rate = (curvature + weathervane_index * np.sin(theta) )

        else:
            turning_rate = curvature
        # Convert curvature to change in direction
        # Curvature is treated as degrees/mm
        angle_change = ( turning_rate * step_size * np.pi / 180)
        direction += angle_change

        # Klinokinesis / Pirouette

        if mechanism in ["klinokinesis", "both"]:

            probability = pirouette_probability(theta)

            if np.random.random() < probability:

                pirouettes += 1

                # Large reorientation.
                # A realistic model would sample this from the experimental turning-angle distribution in Yoshida's Supplementary (Fig S1e)
                # Here approximate it with a random angle between 100 and 180 degrees.

                turn_angle = np.random.uniform(np.deg2rad(100),np.deg2rad(180))

                # Randomly choose left or right
                if np.random.random() < 0.5:
                    turn_angle *= -1

                direction += turn_angle

        # Move forward

        x += step_size * np.cos(direction)
        y +=step_size* np.sin(direction)

    return {
        "x": trajectory_x,
        "y": trajectory_y,
        "concentration": concentrations,
        "pirouettes": pirouettes
    }

# simulate multiple worms

def simulate_population(mechanism, n_worms=N_WORMS):
    worms = []

    for _ in range(n_worms):

        # Random starting y-position
        start_y = np.random.uniform(-10, 10)

        # Random starting direction
        start_direction = np.random.uniform(-np.pi, np.pi)

        worm = simulate_worm(mechanism=mechanism, start_x=0, start_y=start_y, start_direction=start_direction)
        worms.append(worm)

    return worms


# create odour landscape for plotting

def create_landscape():

    x = np.linspace(-5, 20, 150)
    y = np.linspace(-15, 15, 150)

    X, Y = np.meshgrid(x, y)

    C = odour_concentration(X, Y, source_x=10,source_y=0 )
    return X, Y, C

# plot trajectorys

def plot_population(worms, title):

    X, Y, C = create_landscape()
    plt.figure(figsize=(10, 6))
    plt.contourf( X, Y, C, levels=30)
    # Plot only a subset of worms (so the figure is readable)

    for worm in worms[:30]:

        plt.plot(worm["x"], worm["y"],linewidth=0.7, alpha=0.6)

    # Odour source
    plt.scatter( 10, 0,  s=100, marker="*", label="Odour source" )

    plt.xlabel("x position (mm)")
    plt.ylabel("y position (mm)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


# run simulations
if __name__ == "__main__":

    print("Running random walk...")
    random_worms = simulate_population( "random")

    print("Running klinokinesis...")

    klinokinesis_worms = simulate_population("klinokinesis" )

    print("Running klinotaxis...")

    klinotaxis_worms = simulate_population( "klinotaxis" )

    print("Running combined model...")

    combined_worms = simulate_population( "both" )


    # display results

    plot_population( random_worms,"Random walk" )

    plot_population( klinokinesis_worms,"Klinokinesis")

    plot_population( klinotaxis_worms,"Klinotaxis / weathervane")

    plot_population( combined_worms, "Klinokinesis + klinotaxis")
