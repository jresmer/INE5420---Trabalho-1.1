class ColorManager:
    def __init__(self):
        self.__colors = {"Red": "red", 
                         "Blue": "blue", 
                         "Green": "green", 
                         "Yellow": "yellow",
                         "Dark Blue": "blue4"}


    def get_object_color(self, name: str):

        if name in self.__colors:

            return self.__colors[name]
        
        return None
    
    def get_all_object_colors(self):
        colors = list(self.__colors.keys())
        colors.sort()
        return [color for color in colors]
    