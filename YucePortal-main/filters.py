import logging
 
class RequestFilter(logging.Filter):
    def filter(self, record):
        # Exclude logs for specific paths
        if 'GET /static/' in record.getMessage():
            return False
        if 'GET /images/' in record.getMessage():
            return False
        if 'GET /style.css/' in record.getMessage():
            return False
        if 'GET /path-to-your-video.mp4 HTTP/' in record.getMessage():
            return False
        if 'GET /path-to-your-heatmap-image.jpg HTTP/' in record.getMessage():
            return False
        if 'GET /favicon.ico HTTP/' in record.getMessage():
            return False
        return True