from Simulation import Simulation
from Renderer import Renderer

if __name__ == "__main__":
    graphics = True
    simulation = Simulation()
    if graphics:
        renderer = Renderer(simulation)
        renderer.run()
    else:
        simulation.run()
