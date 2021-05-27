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
        self.img = ""
        self.file = ""
        # создаем рабочую область
        self.panel = tkinter.Label(self.root, image=self.img)
        self.panel.pack(anchor='s')
        self.panel.bind('<Button-1>', self.onclick_obj)

        # Добавим метку
        # self.label = tkinter.Label(self.frame, text="Hello, World!").grid(row=1, column=1)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ФАЙЛ", command=self.choose_file_handler).grid(row=1, column=1)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ТЫКАТЬ ФОН", command=self.select_bck_handler).grid(row=1,
                                                                                                            column=2)
        self.but = tkinter.Button(self.panel, text="ХАЧУ ТЫКАТЬ ОБЪЕКТ", command=self.select_obj_handler).grid(row=1,
                                                                                                               column=3)
        self.but = tkinter.Button(self.panel, text="ХАЧУ СЕГМЕНТАЦИЮ!", command=self.segmentation_handler).grid(row=1,
                                                                                                                column=4)

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
            self.obj_pixel_x.append(event.x)
            self.obj_pixel_y.append(event.y)
            print("Объект:", event.x, event.y)
        else:
            self.bck_pixel_x.append(event.x)
            self.bck_pixel_y.append(event.y)
            print("Фон:", event.x, event.y)

    def segmentation_handler(self):
        if len(self.bck_pixel_x) == 0:
            messagebox.showinfo("Ошибка", "Выберите хотя бы одну точку фона")
        elif len(self.obj_pixel_x) == 0:
            messagebox.showinfo("Ошибка", "Выберите хотя бы одну точку объекта")
        else:
            table_x, table_y, table_capacity, height, width = graph_maker.make_graph(self.file, self.bck_pixel_x,
                                                                                     self.bck_pixel_y,
                                                                                     self.obj_pixel_x, self.obj_pixel_y)
            graph = DinitzAlg.Graph(table_x, table_y, table_capacity, height, width)
            graph.dinitz_alg()
            white_pixels_numbers = []
            for i in range(0, len(graph.levels)):
                if graph.levels[i] > -1:
                    white_pixels_numbers.append(i)
            image = graph_maker.get_bwimage(white_pixels_numbers, width, height)
            image.show()
            image.save("result_image6.jpg")


app = App()
