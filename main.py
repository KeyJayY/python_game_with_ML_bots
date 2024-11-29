from simulation import Simulation
from renderer import Renderer

if __name__ == "__main__":
    graphics = True
    simulation = Simulation()
    if graphics:
        renderer = Renderer(simulation) 
        renderer.run()
    else:
        simulation.run()
