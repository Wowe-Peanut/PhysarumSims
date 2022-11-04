
import numpy as np
from PIL import Image

SENSOR_DISTANCE = None
SENSOR_SIZE = None
SENSOR_ANGLE = None
STEP_SIZE = None
ROTATION_ANGLE = None
DEPOSITION_AMOUNT = None
DECAY_FACTOR = None
DEPOSIT_SIZE = None
DIFFUSE_SIZE = None



class Particle:
    def __init__(self, heading: list, position: list):
        self.heading = heading
        self.position = position



class MapData:
    particles = [Particle([0,1], [500, 500])]
    trail_map = [[]]

    #All particles sense ahead & turn accordingly
    def turn_particles(self):
        pass

    #Moves particles in direction of their heading
    def move_particles(self):
        pass 

    #Deposit new particle locations onto trail map
    def deposit(self):
        pass

    #Defuse trail map w/ mean filter then decay cells based
    def defuse_decay(self):
        pass
    
    def tick(self):
        #Steps are seperated to ensure all rules applied uniformly & instantanously, not one cell at a time
        self.turn_particles()
        self.move_particles()
        self.deposit()
        self.defuse_decay()

    #Returns a PIL Image object of the current trailmap 
    def snapshot(self) -> Image:
        pass

    #Creates and saves a video and/or GIF of a sim for a given initial list of particles, and given video specifications
    def simulate(self, initial_state, duration, fps, target_filepath):
        pass

    
def main():
    pass

    

if __name__ == '__main__':
    main()
