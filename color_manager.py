class ColorManager:
    def __init__(self):
        self.__colors = ["Red", "Blue", "Green"]


    def get_object_color(self, name: str):

        if name in self.__colors:

            return self.__colors[name]
        
        return None
    
    def get_all_object_colors(self):

        return [color.lower() for color in self.__colors]
    