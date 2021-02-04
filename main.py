# Main script for 'Solar System Physics 2d' by Sjoerd Vermeulen
# !!! Very amateuristic and inefficient code !!! (i'm new to this)

# ACKNOWLEDGED BUGS/MISSING THINGS:
#   - When really close, to bodies ought to act very wild and sling eachother to unrealistic velicities.
#   - There's no collision yet.
#   - The simulation of gravity with more than 2 bodies might be off. idk.

# ACKNOWLEDGED UPSIDES:
#   - it looks pretty fun ngl.
#   - its my first real coding project so yea.

import pygame, os, time, math, sys, bodies
from bodies import colors
pygame.font.init()
pygame.mixer.init()
pygame.init()
sys.setrecursionlimit(10000)
clock = pygame.time.Clock()

print('\n Launching main.py...\n')

#CONSTANTS
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Physics 2d")
FONT = pygame.font.SysFont(os.path.join('fonts', 'OpenSans-Regular.ttf'), 20)

display_text1 = 'Orbital Physics simulator 2d'

FPS = bodies.settings['FPS']
TRACE_MAX = bodies.settings['TRACE_MAX']
TRACE_DISTANCE = bodies.settings['TRACE_DISTANCE']
SLINGSHOT_RANGE = bodies.settings['SLINGSHOT_RANGE']

G = bodies.settings['G']

#variables:
dt = bodies.settings['dt']
t = 0 #no effect

#mom = math.sqrt(G * star_m / orbit height * body_m**2

traces = []
for body in bodies.bodies.keys():
    color = bodies.bodies[body]['color']
    trace = [color]
    traces.append(trace)
print(f'traces: {traces}')
slingshots = []

run = True
center = 0
showtraces = 0
pause = True


def draw_window(bodies, center, showtraces, slingshots):
    pygame.Surface.fill(WIN, colors['BLACK'])
    if showtraces:
        for trace in traces:
            for pos in trace:
                if len(pos) == 2:
                    if 0 < list(pos_calc(pos, center, 'line 52'))[0] < WIDTH and 0 < list(pos_calc(pos, center, 'line 52'))[1] < HEIGHT:
                        if showtraces == 1:
                            pygame.draw.circle(WIN, trace[0], pos_calc(pos, center, 'line 54'), 1)
                        if len(trace) > 3 and trace.index(pos)-1 > 0 and showtraces == 2:
                            pygame.draw.line(WIN, trace[0], pos_calc(pos, center, 'line 56'), pos_calc(trace[trace.index(pos)-1], center, 'line 56'), 2)
    
        if slingshots:
            for pos in slingshots:
                if 0 < list(pos_calc(pos, center, 'line 60'))[0] < WIDTH and 0 < list(pos_calc(pos, center, 'line 60'))[1] < HEIGHT:
                    pygame.draw.circle(WIN, colors['YELLOW'], pos_calc(pos, center, 'line 61'), 2)
    
    for body in bodies.bodies:
        pygame.draw.circle(WIN, bodies.bodies[body]['color'], pos_calc(bodies.bodies[body]['pos'], center, 'line 64'), bodies.bodies[body]['radius'])
    
    
    text_surface = FONT.render('Orbital Physics simulator 2d: By Sjoerd Vermeulen', False, colors['WHITE'])
    WIN.blit(text_surface, dest=(10,10))
    pygame.draw.line(WIN, colors['WHITE'], (8,28), (330,28), 2)
    
    pygame.display.update()

    
    
def handle_keys(center, showtraces, pause):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            
        if event.type == pygame.KEYUP:
            # fucus next
            if event.key == pygame.K_UP:
                if center < len(bodies.bodies.keys()):
                    center += 1
                else:
                    center = 0
            #focus previous
            if event.key == pygame.K_DOWN:
                if center > 0:
                    center -= 1
                else:
                    center = len(bodies.bodies.keys())
            #toggle traces
            if event.key == pygame.K_t:
                if showtraces == 0:
                    showtraces = 1
                elif showtraces == 1:
                    showtraces = 2
                else:
                    showtraces = 0
            #toggle traces
            if event.key == pygame.K_p:
                if pause:
                    pause = False
                else:
                    pause = True   
                
    keys_pressed = pygame.key.get_pressed()
    return center, showtraces, pause
    

    
    
def pos_calc(pos, center, txt='None'):
    pos = list(pos)
    pos[0] += WIDTH/2
    pos[1] += HEIGHT/2
    
    if center != 0:
        
        centerlist = list(bodies.bodies.keys())
        
        
        pos[0] -= list(bodies.bodies[centerlist[center - 1]]['pos'])[0]
        pos[1] -= list(bodies.bodies[centerlist[center - 1]]['pos'])[1]
    
    pos = tuple(pos)
    return(pos)

def update_fps():
    fps = str(int(clock.get_fps()))
    return fps

#object = [x, y, mass]
def gforce(p1,p2):
    # distance and magnitude and unit vector of distance vector
    dis_vec = ( list(p1)[0] - list(p2)[0] , list(p1)[1] - list(p2)[1] )
    
    dis_mag = magnitude(dis_vec)
    
    dis_hat = ( list(dis_vec)[0] / dis_mag , list(dis_vec)[1] / dis_mag )
    
    # force magnitude
    force_mag = G*p1[2]*p2[2]/dis_mag**2

    # force vector
    force_vec = (force_mag * list(dis_hat)[0] , force_mag * list(dis_hat)[1] )
    
    return force_vec

def magnitude(vec):
    summ = 0
    for i in range(len(vec)):
        summ = vec[i]*vec[i] + summ    
    return pow(summ,0.5)


def all_calc(bodies, slingshots):
    # send body values to gforce function for processing
    for body1 in bodies.bodies.keys():
        #determine p1
        x = list(pos_calc(bodies.bodies[body1]['pos'], center, 'line 164'))[0]
        y = list(pos_calc(bodies.bodies[body1]['pos'], center, 'line 165'))[1]
        p1 = [x, y, bodies.bodies[body1]['mass']] #, bodies.bodies[body1][3]]
        
        for body2 in bodies.bodies.keys():
            if body2 == body1:
                continue
            else:  
                #determine p2
                x = list(pos_calc(bodies.bodies[body2]['pos'], center, 'line 173'))[0]
                y = list(pos_calc(bodies.bodies[body2]['pos'], center, 'line 174'))[1]
                p2 = [x, y, bodies.bodies[body2]['mass']] #, bodies.bodies[body2][3]]
                
                force_vec = gforce(p1, p2)
                #update momentum
                
                bodies.bodies[body2]['mom'] = ( 
                    list(bodies.bodies[body2]['mom'])[0] + list(force_vec)[0] * dt ,
                    list(bodies.bodies[body2]['mom'])[1] + list(force_vec)[1] * dt 
                )
                
                #update position
                #star.pos = star.pos + star.momentum/star.mass*dt
                old_x = list(bodies.bodies[body2]['pos'])[0]
                old_y = list(bodies.bodies[body2]['pos'])[1]
                
                new_x = old_x + list(bodies.bodies[body2]['mom'])[0] / bodies.bodies[body2]['mass']
                new_y = old_y + list(bodies.bodies[body2]['mom'])[1] / bodies.bodies[body2]['mass']
                
                bodies.bodies[body2]['pos'] = (new_x, new_y)
                
                bd_x = list(bodies.bodies[body1]['pos'])[0]
                bd_y = list(bodies.bodies[body1]['pos'])[1]
                
                if math.sqrt( (bd_x - new_x)**2 + (bd_y - new_y)**2 ) < SLINGSHOT_RANGE:
                    slingshots.append( ( ( bd_x + new_x ) / 2 , ( bd_y + new_y ) / 2 ) )
                
    return bodies, slingshots



def main(bodies, center, showtraces, pause):
    
    clock = pygame.time.Clock()
    run = True
    center = 0
    slingshots = []
    
    while run:
        clock.tick(FPS)
        
        center, showtraces, pause = handle_keys(center, showtraces, pause)
        
        if pause:
            #save old pos to trace lists
            trace_id = 0
            for body in bodies.bodies.keys():
                if len(traces[trace_id]) > 1:
                    a_x = round( (list(traces[trace_id][-1])[0]).real , 5 )
                    a_y = round( (list(traces[trace_id][-1])[1]).real , 5 )
                    b_x = round( (list(bodies.bodies[body]['pos'])[0]).real, 5 )
                    b_y = round( (list(bodies.bodies[body]['pos'])[1]).real, 5 )
                
                    if ( math.sqrt((b_x - a_x)**2 + (b_y - a_y)**2) > TRACE_DISTANCE ):
                        traces[trace_id].append(bodies.bodies[body]['pos'])
                    if len(traces[trace_id]) > TRACE_MAX:
                        del traces[trace_id][1]
                else:
                    traces[trace_id].append(bodies.bodies[body]['pos'])
                trace_id = trace_id + 1
        
            bodies, slingshots = all_calc(bodies, slingshots)
        draw_window(bodies, center, showtraces, slingshots)
    
    main(bodies, center, showtraces)


if __name__ == "__main__":
    main(bodies, center, showtraces, pause)

