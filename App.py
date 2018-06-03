import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from text_recognition import FormParser


class App:
    def __init__(self, root):
        self.root = root
        self.choose_image_button = tk.Button(root, text="Выбрать файл с изображением бланка", command=self.open_image).pack()
        self.choose_network_button = tk.Button(root, text="Выбрать файл с обученной нейронной сетью", command=self.open_network).pack()
        self.recognition_button = tk.Button(root, text="Распознать текст", command=self.recognise).pack()
        self.answer = tk.StringVar()
        self.answer_label = tk.Label(root, textvariable=self.answer, bg="white").pack()
        self.image_label = tk.Label(self.root)
        self.text = None
        self.img_path = None
        self.network_path = None

    def open_image(self):
        file = filedialog.askopenfile(initialdir='C:\\Users\\User\\Desktop\\Thesis\\forms')
        try:
            size = 400, 300
            img = Image.open(file.name, 'r')
            img = img.resize(size, Image.ANTIALIAS)
            self.image_label.pack_forget()
            self.image_label.image = ImageTk.PhotoImage(img)
            self.image_label['image'] = self.image_label.image
            self.image_label.pack(side="top", fill="both", expand="yes")
            self.img_path = file.name
        except AttributeError:
            messagebox.showerror('', 'Файл не выбран!')

    def open_network(self):
        file = filedialog.askopenfile(initialdir='C:\\Users\\User\\Desktop\\Thesis\\trained_nn\\own_data237')
        try:
            self.network_path = file.name[:-5]
            messagebox.showinfo('', 'Файл с нейронной сетью успешно выбран!')
        except AttributeError:
            messagebox.showerror('', 'Файл не выбран!')

    def recognise(self):
        parser = FormParser.FormParser(self.img_path)
        parser.get_chars()
        parser.cut_borders(parser.name_path)
        parser.cut_borders(parser.second_name_path)
        parser.delete_empty(parser.name_path)
        parser.delete_empty(parser.second_name_path)
        first, second = parser.get_full_name(self.network_path)
        self.text = first + ' ' + second
        self.display_recognised_text()

    def display_recognised_text(self):
        self.answer.set(self.text)


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("600x450")
    window.title("Text recognition application")
    obj = App(window)
    window.mainloop()
