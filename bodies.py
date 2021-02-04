# Variables of 'Solar System Physics 2d' by Sjoerd Vermeulen
# I DO NOT RECCOMMEND CHANGING ANYTHING ELSE THAN THE VALUES

# The colors available: (custom ones can be added but keep them correctly formatted.)
# format:   'COLOR' : (rbg values),
colors = {
    'WHITE' : (255, 255, 255),
    'BLACK' : (0, 0, 0),
    'RED' : (255, 0, 0),
    'GREEN' : (0, 255, 0),
    'BLUE' : (0, 0, 225),
    'YELLOW' : (255, 255, 0),
    'ORANGE' : (255,165,0),
}

# The simulation settings.
settings = {
    'G' : 3,                # grav. constant. feel free to change
    'dt' : 1,               # some time unit. don't reccomend changing it
    'FPS' : 60,             # fps
    'TRACE_DISTANCE' : 8,   # distance between trajectory tracing points
    'TRACE_MAX' : 200,      # maximum tracing points (less than 400 is reccomended)
    'SLINGSHOT_RANGE' : 20, # range at which a grav. slingshot is detected
}

# List of bodies in simulation (feel free to add and customize any body but keep it formatted.
# body color must be in the colors dict up above!
bodies = {
    'body_0' : {
        'name' : 'sun',
        'color' : colors['ORANGE'],
        'pos' : (0,0),
        'radius' : 30,
        'mass' : 2.0*1000,
        'mom' : (0,0),
    },
    'body_1' : {
        'name' : 'blue',
        'color' : colors['BLUE'],
        'pos' : (200,0),
        'radius' : 10,
        'mass' : 10,
        'mom' : (0,40),
    },
    'body_2' : {
        'name' : 'green',
        'color' : colors['GREEN'],
        'pos' : (-200,0),
        'radius' : 10,
        'mass' : 10,
        'mom' : (0,-30),
    },
    'body_3' : {
        'name' : 'white',
        'color' : colors['WHITE'],
        'pos' : (-400,0),
        'radius' : 10,
        'mass' : 10,
        'mom' : (0,-10),
    },
}

# import confirmation message
print('succesfully imported module Bodies.')