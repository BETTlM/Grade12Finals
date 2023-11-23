import math

from tkinter import Canvas

class GradientFrame(Canvas):
    
    """
    Widget with gradient colors.
    """

    __tag = "GradientFrame"
    __hex_format = "#%04x%04x%04x"
    
    top2bottom = 1
    left2right = 2

    def __init__(self, parent, colors = ("red", "black"), direction = left2right, **kw):

        kw["height"] = kw.get("height", 200)
        kw["width"] = kw.get("width", 200)
        
        super().__init__(parent, **kw)

        self.__geometry = [kw["width"], kw["height"]]
        self.__colors = colors
        self.__direction = direction

        
        self.__draw_gradient()
        
    def __draw_gradient(self):
        
        """
        Paint the Canvas with gradient colors.
        """

        
        self.delete(self.__tag)

        limit = self.__geometry[0] if self.__direction == self.left2right else self.__geometry[1]
       
        
        red1, green1, blue1 = self.winfo_rgb(self.__colors[0])
        red2, green2, blue2 = self.winfo_rgb(self.__colors[1])

        
        r_ratio = (red2 - red1) / limit
        g_ratio = (green2 - green1) / limit
        b_ratio = (blue2 - blue1) / limit

        for pixel in range(limit):
            
            red = int(red1 + (r_ratio * pixel))
            green = int(green1 + (g_ratio * pixel))
            blue = int(blue1 + (b_ratio * pixel))

            color = self.__hex_format % (red, green, blue)

            x1 = pixel if self.__direction == self.left2right else 0
            y1 = 0 if self.__direction == self.left2right else pixel
            
            x2 = pixel if self.__direction == self.left2right else self.__geometry[0]
            y2 = self.__geometry[1] if self.__direction == self.left2right else pixel

            self.create_line(x1, y1, x2, y2, tag = self.__tag, fill = color)

        self.tag_lower(self.__tag)

    
    def config(self, cnf = None, **kw):

        if "colors" in kw and len(kw["colors"]) > 1:
            self.__colors = kw.pop("colors")

        if "direction" in kw and kw["direction"] in (self.left2right, self.top2bottom):
            self.__direction = kw.pop("direction")

        if "height" in kw:
            self.__geometry[1] = kw["height"]

        if "width" in kw:
            self.__geometry[0] = kw["width"]

        
        super().config(cnf, **kw)
        self.__draw_gradient()

  
    def configure(self, cnf = None, **kw):
        self.config(cnf, **kw)