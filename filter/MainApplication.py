import Image as Im
import Filter as Fil
import Tkinter as tk
from tkFileDialog import askopenfilename


class MainApplication: 
    def __init__(self, master):
        self.master = master
        self.master.title("Filter program")
        self.frame = tk.Frame(self.master, width=500, height=300)
        self.frame.pack(expand=tk.YES)
        self.create_widgets()


    def create_widgets(self):
        self.label = tk.Label(self.frame, text="Have fun with filters!")
        self.label.pack()

        self.open_button = tk.Button(self.frame, text="Load image (gif)", width=25, command=self.open_picture)
        self.open_button.pack()

        self.quit_button = tk.Button(self.frame, text="Exit", width=25, command=self.master.quit)
        self.quit_button.pack()

        self.interaction_label = tk.Label(self.frame)

        self.filter_box = tk.Button(self.master, text="Box filter", width=20, command=self.box_filter)
        self.filter_sharpen = tk.Button(self.master, text="Sharpen filter", width=20, command=self.sharpen_filter)
        self.filter_median = tk.Button(self.master, text="Median filter", width=20, command=self.median_filter)
        self.original = tk.Button(self.master, text="Original", width=20, command=self.set_original)


    def set_original(self):
        self.canvas.create_image(25, 25, anchor=tk.NW, image=self.img)
        self.canvas.update()


# the filters
    def median_filter(self):
        self.original.pack(padx="10", pady="10", side=tk.LEFT)  # Button for original img
        if hasattr(self, 'median_pic'):  # show already saved, filtered img on button click
            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.median_pic)
            self.canvas.update()
        else:
            image = Im.Image(self.filename, self.img.copy())
            filter = Fil.Filter(image.get_pixel_matrix(), image)
            self.median_pic = filter.median_filter()

            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.median_pic)
            self.canvas.update()


    def sharpen_filter(self):
        self.original.pack(padx="10", pady="10", side=tk.LEFT)
        if hasattr(self, 'sharp_pic'):
            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.sharp_pic)
            self.canvas.update()
        else:
            image = Im.Image(self.filename, self.img.copy())
            filter = Fil.Filter(image.get_pixel_matrix(), image)
            self.sharp_pic = filter.sharpen_filter()

            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.sharp_pic)
            self.canvas.update()


    def box_filter(self):
        self.original.pack(padx="10", pady="10", side=tk.LEFT)
        if hasattr(self, 'box_filter_pic'):
            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.box_filter_pic)
            self.canvas.update()
        else:
            image = Im.Image(self.filename, self.img.copy())
            filter = Fil.Filter(image.get_pixel_matrix(), image)
            self.box_filter_pic = filter.box_filter()

            self.canvas.create_image(25, 25, anchor=tk.NW, image=self.box_filter_pic)
            self.canvas.update()


# open images and dynamic GUI changes 
    def open_picture(self):
        if hasattr(self, 'img'):  # if an img was already loaded
            self.canvas.delete("all")  # clean canvas
            self.original.forget()  # hide 'Original' button
            self.filename = askopenfilename(initialdir="/", title="Choose file",
                                            filetypes=(("GIF files", "*.gif"), ('All files', '.*')))
            #  if no img was loaded, hide filter buttons
            if self.filename == '':
                print "No image loaded."
                self.filter_box.forget()
                self.filter_sharpen.forget()
                self.filter_median.forget()
            else:  # if not, load new img and update canvas 
                self.img = tk.PhotoImage(file=self.filename)
                self.canvas.config(width=self.img.width(), height=self.img.height())
                self.canvas.create_image(25, 25, anchor=tk.NW, image=self.img)
                self.canvas.update()
                #  show buttons in case they were hidden
                self.filter_box.pack(padx="10", pady="10", side=tk.LEFT)
                self.filter_sharpen.pack(padx="10", pady="10", side=tk.LEFT)
                self.filter_median.pack(padx="10", pady="10", side=tk.LEFT)

            # delete saved images to load new img
            if hasattr(self, "median_pic"):
                del (self.median_pic)
            if hasattr(self, "box_filter_pic"):
                del (self.box_filter_pic)
            if hasattr(self, "sharp_pic"):
                del (self.sharp_pic)
        else:  # if no img was loaded, pack() canvas
            self.filename = askopenfilename(initialdir="/", title="Choose file",
                                            filetypes=(("GIF files", "*.gif"), ('All files', '.*')))
            if self.filename == '':
                print "No image loaded."
            else:
                self.img = tk.PhotoImage(file=self.filename)
                self.canvas = tk.Canvas(self.master, width=self.img.width(), height=self.img.height())
                self.canvas.create_image(25, 25, anchor=tk.NW, image=self.img)

                self.canvas.pack()

                self.filter_box.pack(padx="10", pady="10", side=tk.LEFT)
                self.filter_sharpen.pack(padx="10", pady="10", side=tk.LEFT)
                self.filter_median.pack(padx="10", pady="10", side=tk.LEFT)


root = tk.Tk()
root.minsize(width=300, height=150)
app = MainApplication(root)
root.mainloop()

