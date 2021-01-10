import uuid
import datetime


def upload_image(instance, file):
    today = datetime.datetime.now()
    final_path = '/'.join(['gallery', str(instance._meta.model_name), str(uuid.uuid4()) + str(file.split('.')[:-1]) +"."+ str(file.split('.')[-1])])
    return final_path


from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians(52.2296756)
lon1 = radians(21.0122287)
lat2 = radians(52.406374)
lon2 = radians(16.9251681)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)