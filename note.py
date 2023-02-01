import os

class Note:
    def __init__(self,name,c=""):
        self.name:str = name
        self.ext:str = ".txt"
        self.content:str = c
        
    def save(self,dir):
        with open(f"{dir}/{self.name}{self.ext}","w") as file:
            file.write(self.content)
    
    def rename(self,name):
        self.name = name
        
    def load(self,content):
        self.content = content
        
class Book:
    
    def __init__(self,name):
        self.name:str=name
        self.pages:list[Note] = list()
        self.add()
        
    def rename(self,name):
        self.name = name
        
    def get(self,pageIndex):
        for p in self.pages:
            if p.name == str(pageIndex):
                return p.content
            
    def add(self,content=""):
        new = Note(self.pages.__len__(),content)
        self.pages.append(new)
        
    def save(self,dir):
        newdir = dir+"/"+self.name
        if not os.path.exists(newdir):
            os.mkdir(newdir)
        for p in self.pages:
            p.save(newdir)