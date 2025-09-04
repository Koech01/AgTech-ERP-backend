import uuid

def profileIconUID(instance, filename):
    fileExt  = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{fileExt}'
    return f'ProfileIcons/{filename}'