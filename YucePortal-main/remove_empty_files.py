import os

def remove_empty_files(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            
            if file_size == 0:
                os.remove(file_path)
