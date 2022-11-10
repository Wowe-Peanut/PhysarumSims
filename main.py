
import numpy as np
from PIL import Image
import imageio
import random
import math

SENSOR_DISTANCE = 1
SENSOR_SIZE = 1
SENSOR_ANGLE = math.pi/4

STEP_SIZE = 1
ROTATION_ANGLE = math.pi/4

DEPOSITION_AMOUNT = 255
DECAY_FACTOR = 0.9
DEPOSIT_SIZE = 1
DIFFUSE_SIZE = None



class Particle:
    def __init__(self, heading: list, position: list):
        self.heading = np.asarray(heading)
        self.pos = np.asarray(position)
        self.set_sensor_positions()

    def step(self, map_size):
        old_pos = self.pos.copy()

        #Move along heading & bound to map size
        self.pos = np.add(self.pos, STEP_SIZE*self.heading)
        self.pos[0] = max(0, min(self.pos[0], map_size[0]-1))
        self.pos[1] = max(0, min(self.pos[1], map_size[1]-1))

        #Move sensors along same heading but only for as far self.pos moved
        deltaP = self.pos-old_pos
        self.sensor_positions = [np.add(sensor, deltaP) for sensor in self.sensor_positions]
               
    def set_sensor_positions(self):
        front = SENSOR_DISTANCE*self.heading
        left = np.dot(front, self.get_rotation_matrix(-SENSOR_ANGLE))
        right = np.dot(front, self.get_rotation_matrix(SENSOR_ANGLE))
        self.sensor_positions = [left, front, right]

    def get_rotation_matrix(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array(((c, -s),(s, c)))

    def rotate(self, theta):
        self.heading = np.dot(self.heading, self.get_rotation_matrix(theta))
        self.set_sensor_positions()



class MapData:
    particles = []
    trail_map = []
    frames = []

    def __init__(self, size=(50, 50)):
        self.size = size
        self.trail_map = np.zeros(size)

    #All particles sense ahead & turn accordingly
    def turn_particles(self):
        for p in self.particles:
            #Global sensor positions
            gsps = [np.add(p.pos, s) for s in p.sensor_positions]
            
            #Sensor values
            svals = [0 if not (0 <= round(gsp[0]) < self.size[0] and 0 <= round(gsp[1]) < self.size[1]) else self.trail_map[round(gsp[0]), round(gsp[1])] for gsp in gsps]

            p.rotate((svals.index(max(svals))-1)*ROTATION_ANGLE)


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
        self.turn_particles()
        
        #Step
        for p in self.particles:
            p.step(self.size)

        #Deposit
        for p in self.particles:
            self.trail_map[int(p.pos[0]), int(p.pos[1])] = DEPOSITION_AMOUNT

        self.defuse()

        #Decay
        self.trail_map *= DECAY_FACTOR
        self.trail_map[self.trail_map < 1] = 0

    #Returns a PIL Image object of the current trailmap 
    def snapshot(self) -> Image:
        return Image.fromarray(self.trail_map).resize((2000,2000), Image.Resampling.NEAREST)
        
    #Creates and saves a video and/or GIF of a sim for a given initial list of particles, and given video specifications
    def simulate(self, starting_particles, duration, fps, tpf):
        self.particles = starting_particles

        for frame in range(fps*duration):
            print(frame)
            for t in range(tpf):
                self.tick()
            self.frames.append(self.snapshot())
        
        imageio.mimsave(r"C:\Users\Peanu\OneDrive\Desktop\Github\PhysarumSims\{0}.gif".format(random.randint(0, 2**31-1)), self.frames, duration=(1/fps))
            
        
        

   
def main():
    test = MapData((400,400))
    starting_particles = [Particle([math.cos(theta), math.sin(theta)],[random.randint(0,100),random.randint(0, 100)]) for theta in [2*math.pi*random.random() for i in range(10000)]]
    test.simulate(starting_particles, 5, 30, 1)


if __name__ == '__main__':
    main()
