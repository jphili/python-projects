from Tkinter import PhotoImage


class Filter:
    def __init__(self, pixel_matrix, image):
        self.pixel_matrix = pixel_matrix
        self.width = image.picture_width()
        self.height = image.picture_height()
        self.image = image

    def box_filter(self):
        print "Box filter is used..."
        box_filter_pic = PhotoImage(width=self.width, height=self.height)  # preserve dimensions of orig. img

        for v in range(0, self.height):
            for u in range(0, self.width):
                summe = [0, 0, 0]  # create a filter region for every pixel
                for j in range(-1, 2):  # move filter
                    for i in range(-1, 2):
                        if 0 <= u + i < self.width:
                            if 0 <= v + j < self.height:
                                pixel = map(int, self.pixel_matrix[u + i][v + j].split())
                                summe = [sum([x, y]) for x, y in zip(pixel, summe)]
                            else:
                                pixel = map(int, self.pixel_matrix[u][v - 1].split())  # fill edge pixel
                                summe = [sum([x, y]) for x, y in zip(pixel, summe)]
                        else:
                            pixel = map(int, self.pixel_matrix[u - 1][v].split())  # fill edge pixel
                            summe = [sum([x, y]) for x, y in zip(pixel, summe)]
                r, g, b = [x / 9.0 for x in summe]
                box_filter_pic.put("#%02x%02x%02x" % (int(r), int(g), int(b)), (u, v))
        print "Done!\n"
        return box_filter_pic

    def sharpen_filter(self):
        print "Sharpen filter is used..."
        sharp_pic = PhotoImage(width=self.width, height=self.height)  

        filter_region = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
        for v in range(0, self.height):
            for u in range(0, self.width):
                summe_Rp = [0, 0, 0]
                summe_Rm = [0, 0, 0]
                for j in range(-1, 2):  
                    for i in range(-1, 2):
                        filter_co = filter_region[j + 1][i + 1]
                        if 0 <= u + i < self.width:
                            if 0 <= v + j < self.height:
                                pixel = map(int, self.pixel_matrix[u + i][v + j].split())
                                if filter_co > 0:
                                    help = [x * filter_co for x in pixel]
                                    summe_Rp = [sum([x, y]) for x, y in zip(help, summe_Rp)]
                                else:
                                    help = [x * abs(filter_co) for x in pixel]
                                    summe_Rm = [sum([x, y]) for x, y in zip(help, summe_Rm)]
                            else:
                                pixel = map(int, self.pixel_matrix[u][v - 1].split())  
                                if filter_co > 0:
                                    help = [x * filter_co for x in pixel]
                                    summe_Rp = [sum([x, y]) for x, y in zip(help, summe_Rp)]
                                else:
                                    help = [x * (filter_co) for x in pixel]
                                    summe_Rm = [sum([x, y]) for x, y in zip(help, summe_Rm)]
                        else:
                            pixel = map(int, self.pixel_matrix[u - 1][v].split())  
                            if filter_co > 0:
                                help = [x * filter_co for x in pixel]
                                summe_Rp = [sum([x, y]) for x, y in zip(help, summe_Rp)]
                            else:
                                help = [x * abs(filter_co) for x in pixel]
                                summe_Rm = [sum([x, y]) for x, y in zip(help, summe_Rm)]

                r, g, b = [x - y for x, y in zip(summe_Rp, summe_Rm)]

                # pixel value range for too high/too low values 
                if int(r) < 0:
                    r = 0
                if int(g) < 0:
                    g = 0
                if int(b) < 0:
                    b = 0

                if int(r) > 255:
                    r = 255
                if int(g) > 255:
                    g = 255
                if int(b) > 255:
                    b = 255

                sharp_pic.put("#%02x%02x%02x" % (int(r), int(g), int(b)), (u, v))
        print "Done!\n"
        return sharp_pic

    def median_filter(self):
        print "Median filter is used..."
        medianpic = PhotoImage(width=self.width, height=self.height)  

        for v in range(0, self.height):
            for u in range(0, self.width):
                filter_region = []  
                for j in range(-1, 2):  
                    for i in range(-1, 2):
                        if 0 <= u + i < self.width:
                            if 0 <= v + j < self.height:
                                filter_region.append(self.pixel_matrix[u + i][v + j])
                            else:
                                filter_region.append(self.pixel_matrix[u][v - 1])  
                        else:
                            filter_region.append(self.pixel_matrix[u - 1][v])  
                filter_region.sort()
                r, g, b = filter_region[4].split()
                medianpic.put("#%02x%02x%02x" % (int(r), int(g), int(b)), (u, v))
        print "Done!\n"
        return medianpic

