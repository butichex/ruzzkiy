from selenium.common.exceptions import * 

class noVideos(BaseException): 
    def __init__(self, username): 
        self.username = username
        
        
    def __str__(self): 
        return f"У пользователя {self.username} нет ни одного видео."
    
