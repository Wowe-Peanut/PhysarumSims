
import numpy as np
from PIL import Image
import imageio
import random
import math

SENSOR_DISTANCE = 1
SENSOR_SIZE = 1
SENSOR_ANGLE = None

STEP_SIZE = 1
ROTATION_ANGLE = None

DEPOSITION_AMOUNT = 255
DECAY_FACTOR = 0.9
DEPOSIT_SIZE = 1
DIFFUSE_SIZE = None



class Particle:
    def __init__(self, heading: list, position: list):
        self.heading = np.asarray(heading)
        self.pos = np.asarray(position)
        self.sensors = []

    def step(self, size):
        self.pos = np.add(self.pos, STEP_SIZE*self.heading)
        self.pos[0] = max(0, min(self.pos[0], size[0]-1))
        self.pos[1] = max(0, min(self.pos[1], size[1]-1))
            
    
    class Sensor:
        def __init__(self):
            pass




class MapData:
    particles = []
    trail_map = []
    frames = []

    def __init__(self, size=(50, 50)):
        self.size = size
        self.trail_map = np.zeros(size)

    #All particles sense ahead & turn accordingly
    def turn_particles(self):
        pass
            



    #Moves particles in direction of their heading
    def move_particles(self):
        for p in self.particles:
            p.step(self.size)
            
    #Deposit new particle locations onto trail map
    def deposit(self):
        for p in self.particles:
            self.trail_map[int(p.pos[0]), int(p.pos[1])] = DEPOSITION_AMOUNT

    #Defuse trail map w/ mean filter then decay cells based
    def defuse(self):
        new_map = np.zeros(self.size)

        #Defuse
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                count = 0
                for rr in range(r-1, r+2):
                    for cc in range(c-1, c+2):
                        if 0 <= rr < self.size[0] and 0 <= cc < self.size[1]:
                            new_map[r,c] += self.trail_map[rr,cc]
                            count += 1
                
                new_map[r,c] /= count

        
        
        self.trail_map = new_map
        
    def tick(self):
        #Steps are seperated to ensure all rules applied uniformly & instantanously, not one cell at a time
        self.turn_particles()
        self.move_particles()
        self.deposit()
        self.defuse()

        #Decay
        self.trail_map *= DECAY_FACTOR

    #Returns a PIL Image object of the current trailmap 
    def snapshot(self) -> Image:
        return Image.fromarray(self.trail_map).resize((2000,2000), Image.Resampling.NEAREST)
        
    #Creates and saves a video and/or GIF of a sim for a given initial list of particles, and given video specifications
    def simulate(self, starting_particles, duration, fps, tpf):
        self.particles = starting_particles

        for frame in range(fps*duration):
            for t in range(tpf):
                self.tick()
            self.frames.append(self.snapshot())
        
        imageio.mimsave(r"C:\Users\Peanu\OneDrive\Desktop\Github\PhysarumSims\{0}.gif".format(random.randint(0, 2**31-1)), self.frames, duration=(1/fps))
            
        
        


    
def main():
    test = MapData((50,50))
    starting_particles = [Particle([math.cos(theta), math.sin(theta)],[random.randint(0,50),random.randint(0,50)]) for theta in [2*math.pi*random.random() for i in range(50)]]
    test.simulate(starting_particles, 10, 10, 1)
    
    

if __name__ == '__main__':
    main()
