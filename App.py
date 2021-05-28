import tkinter
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import graph_maker
import DinitzAlg


class App:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('1400x600')
        self.is_obj = True
        self.obj_pixel_x = []
        self.obj_pixel_y = []
        self.bck_pixel_x = []
        self.bck_pixel_y = []
        self.add_obj_pixel_x = []
        self.add_obj_pixel_y = []
        self.add_bck_pixel_x = []
        self.add_bck_pixel_y = []
        self.segmented = False
        self.img = ""
        self.file = ""
        self.lmbda = 1
        self.sigma = 30
        # создаем рабочую область
        self.panel = tkinter.Label(self.root, image=self.img)
        self.panel.pack(anchor='s')
        self.panel.bind('<Button-1>', self.onclick_obj)

        # Добавим метку
        self.but = tkinter.Button(self.panel, text="ХАЧУ ФАЙЛ", command=self.choose_file_handler).grid(row=1, column=1)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ТЫКАТЬ ФОН", command=self.select_bck_handler).grid(row=1,
                                                                                                            column=2)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ТЫКАТЬ ОБЪЕКТ", command=self.select_obj_handler).grid(row=1,
                                                                                                               column=3)
        self.but = tkinter.Button(self.panel, text="ХАЧУ СЕГМЕНТАЦИЮ!", command=self.segmentation_handler).grid(row=1,
                                                                                                                column=4)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ПЕРЕДЕЛАТЬ!", command=self.recompute_handler).grid(row=1,
                                                                                                            column=5)

        self.root.mainloop()

    def choose_file_handler(self):
        self.file = filedialog.askopenfilename()
        self.img = ImageTk.PhotoImage(Image.open(self.file))
        self.panel = tkinter.Label(self.root, image=self.img)
        self.panel.pack(anchor='s', side="top")
        self.panel.bind('<Button-1>', self.onclick_obj)

    def select_bck_handler(self):
        self.is_obj = False

    def select_obj_handler(self):
        self.is_obj = True

    def onclick_obj(self, event):
        if self.is_obj:
            if self.segmented:
                self.add_obj_pixel_x.append(event.x)
                self.add_obj_pixel_y.append(event.y)
            self.obj_pixel_x.append(event.x)  # Влом исправлять огромную функцию в graph_maker
            self.obj_pixel_y.append(event.y)
            print("Объект:", event.x, event.y)
        else:
            if self.segmented:
                self.add_bck_pixel_x.append(event.x)
                self.add_bck_pixel_y.append(event.x)
            self.bck_pixel_x.append(event.x)
            self.bck_pixel_y.append(event.y)
            print("Фон:", event.x, event.y)

    def segmentation_handler(self):
        table_x, table_y, table_capacity, height, width, obj_prob_func, bck_prob_func, k_edge = graph_maker.make_graph(
            self.file, self.bck_pixel_x, self.bck_pixel_y, self.obj_pixel_x, self.obj_pixel_y, self.lmbda, self.sigma)
        self.graph = DinitzAlg.Graph(table_x, table_y, table_capacity, height, width, Image.open(self.file), k_edge)
        self.graph.dinitz_alg()
        white_pixels_numbers = []
        for i in range(0, len(self.graph.levels)):
            if self.graph.levels[i] > -1:
                white_pixels_numbers.append(i)
        image = graph_maker.get_bwimage(white_pixels_numbers, width, height)
        image.show()
        self.segmented = True
        image.save("result_image6.jpg")

    def recompute_handler(self):
        bck_pix = []
        obj_pix = []
        for i in range(len(self.add_bck_pixel_x)):
            bck_pix.append(self.add_bck_pixel_x[i] * self.graph.width + self.add_bck_pixel_y[i] + 1)
        for i in range(len(self.add_obj_pixel_x)):
            obj_pix.append(self.add_obj_pixel_x[i] * self.graph.width + self.add_obj_pixel_y[i] + 1)
        bck_prob_func = graph_maker.get_histogram_distribution(self.bck_pixel_x, self.bck_pixel_y, Image.open(self.file).load(), self.lmbda)
        obj_prob_func = graph_maker.get_histogram_distribution(self.obj_pixel_x, self.obj_pixel_y, Image.open(self.file).load(), self.lmbda)
        self.graph.recompute_list(obj_pix, bck_pix, bck_prob_func, obj_prob_func)
        self.graph.dinitz_alg()
        self.add_bck_pixel_x = []
        self.add_bck_pixel_y = []
        self.add_obj_pixel_x = []
        self.add_obj_pixel_y = []
        white_pixels_numbers = []
        for i in range(0, len(self.graph.levels)):
            if self.graph.levels[i] > -1:
                white_pixels_numbers.append(i)
        image = graph_maker.get_bwimage(white_pixels_numbers, self.graph.width, self.graph.height)
        image.show()
        image.save("result_image6.jpg")


app = App()
