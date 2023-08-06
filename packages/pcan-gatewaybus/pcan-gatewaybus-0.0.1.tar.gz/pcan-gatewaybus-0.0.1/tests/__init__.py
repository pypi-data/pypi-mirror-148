import can
from can.interface import BACKENDS

def check_backends():
    for key, value in BACKENDS.items():
        if key == 'gateway':
            return True

    return False 

print (check_backends())