import uuid
import datetime


def upload_image(instance, file):
    today = datetime.datetime.now()
    final_path = '/'.join(['gallery', str(instance._meta.model_name), str(uuid.uuid4()) + str(file.split('.')[:-1]) +"."+ str(file.split('.')[-1])])
    return final_path
