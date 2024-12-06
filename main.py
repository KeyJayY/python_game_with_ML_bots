from game.simulation import Simulation
from game.renderer import Renderer

if __name__ == "__main__":
    graphics = True
    simulation = Simulation()
    if graphics:
        renderer = Renderer(simulation)
        renderer.run()
    else:
        simulation.run()
