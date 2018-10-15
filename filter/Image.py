class Image:
    
    def __init__(self, filename, image):
        self.filename = filename
        self.image = image


    def name(self):
        return self.filename


    def picture_width(self):
        return self.image.width()


    def picture_height(self):
        return self.image.height()


    def get_pixel_matrix(self):
        u = self.picture_width()  # M
        v = self.picture_height()  # N
        pixel_matrix = [[self.image.get(x, y) for y in range(v)] for x in range(u)]
        return pixel_matrix

