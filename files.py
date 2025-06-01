
def is_image(file):
    return file.is_file() and file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'))

def is_video(file):
    return file.is_file() and file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'))

def images_in_dir(dir):
    return [file for file in dir.iterdir() if is_image(file)]

def jsons_in_dir(dir):
    return [file for file in dir.iterdir() if file.is_file() and file.name.lower().endswith('.json')]
