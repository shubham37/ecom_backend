import uuid
import datetime


def upload_image(instance, image):
    today = datetime.datetime.now()
    final_path = '/'.join(['gallery', str(instance._meta.model_name), str(uuid.uuid4()) + str(image.split('.')[:-1]) +"."+ str(image.split('.')[-1])])
    return final_path
