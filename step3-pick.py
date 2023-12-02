import os
import shutil
from tkinter import Tk, Label, Button, Canvas, PhotoImage
from tkinter import filedialog

class ImagePickerApp:
    def __init__(self, root, folder_path):
        self.root = root
        self.root.title("Image Picker")
        self.folder_path = folder_path
        self.subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        self.current_folder_index = 0
        self.current_image_index = 0

        self.label_folder_name = Label(root, text=self.subfolders[self.current_folder_index])
        self.label_folder_name.pack()

        self.canvas = Canvas(root, width=1280, height=512)
        self.canvas.pack()

        self.load_images()
        self.display_images()

        # self.button_next = Button(root, text="Next", command=self.next_folder)
        # self.button_next.pack()

        self.root.mainloop()

        self.image_objects = []

    def load_images(self):
        self.images = []
        for folder in self.subfolders:
            folder_path = os.path.join(self.folder_path, folder)
            image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            self.images.append(image_paths)

    def display_images(self):
        self.canvas.delete("all")
        folder = self.subfolders[self.current_folder_index]
        images = self.images[self.current_folder_index]
        self.image_objects = []  # 清空之前的 PhotoImage 对象

        image_width = 256
        image_height = 256
        gap = 0
        max_columns = 5
        total_rows = (len(images) + max_columns - 1) // max_columns

        for i, image_path in enumerate(images):
            if "picked" not in image_path:
                row = i // max_columns
                col = i % max_columns
                x = col * (image_width + gap)
                y = row * (image_height + gap)
                img = PhotoImage(file=image_path)
                img = img.subsample(img.height() // image_height)
                self.image_objects.append(img)
                self.canvas.create_image(x, y, anchor='nw', image=img, tags=("image%d" % i,))
                self.canvas.tag_bind("image%d" % i, "<Button-1>", lambda event, index=i: self.image_clicked(index))
                print("displayed idx: %d; path: %s" % (i, image_path))

    def image_clicked(self, index):
        folder = self.subfolders[self.current_folder_index]
        source_path = self.images[self.current_folder_index][index]
        destination_path = os.path.join(self.folder_path, folder, "picked.png")

        print("selected idx: %d; path: %s" % (index, source_path))

        # Copy the selected image to the folder with the name "picked.png"
        shutil.copyfile(source_path, destination_path)

        self.next_folder()

    def next_folder(self):
        self.current_folder_index += 1

        if self.current_folder_index == len(self.subfolders):
            self.root.destroy()
        else:
            self.label_folder_name.config(text=self.subfolders[self.current_folder_index])
            self.display_images()

if __name__ == "__main__":
    root = Tk()
    # root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        app = ImagePickerApp(root, folder_path)
