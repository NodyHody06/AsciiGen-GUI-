import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
from PIL import Image, ImageFont, ImageDraw
from rembg import remove
import resize as RS
import pixel_mapping as PM

class ASCIIImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Image Generator")

        # Variables
        self.file_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.scaleFactor_var = tk.DoubleVar(value=0.4)
        self.oneCharWidth_var = tk.IntVar(value=12)
        self.oneCharHeight_var = tk.IntVar(value=18)
        self.fontSize_var = tk.IntVar(value=30)
        self.remove_bg_var = tk.BooleanVar()
        self.color_mode_var = tk.StringVar(value="Keep Original Color")

        # GUI Elements
        tk.Label(root, text="Select Input Image:").grid(row=0, column=0, padx=10, pady=10)
        self.file_entry = tk.Entry(root, textvariable=self.file_path_var, width=50)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.select_file).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=10)
        self.output_entry = tk.Entry(root, textvariable=self.output_path_var, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.select_output_folder).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Scale Factor:").grid(row=2, column=0, padx=10, pady=10)
        self.scaleFactor_scale = ttk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.scaleFactor_var, command=self.update_scaleFactor_label)
        self.scaleFactor_scale.grid(row=2, column=1, padx=10, pady=10)
        self.scaleFactor_label = tk.Label(root, text="Scale Factor: 0.4")
        self.scaleFactor_label.grid(row=2, column=2, padx=10, pady=10)

        tk.Label(root, text="Character Width:").grid(row=3, column=0, padx=10, pady=10)
        self.oneCharWidth_scale = ttk.Scale(root, from_=5, to=20, orient=tk.HORIZONTAL, variable=self.oneCharWidth_var, command=self.update_oneCharWidth_label)
        self.oneCharWidth_scale.grid(row=3, column=1, padx=10, pady=10)
        self.oneCharWidth_label = tk.Label(root, text="Character Width: 12")
        self.oneCharWidth_label.grid(row=3, column=2, padx=10, pady=10)

        tk.Label(root, text="Character Height:").grid(row=4, column=0, padx=10, pady=10)
        self.oneCharHeight_scale = ttk.Scale(root, from_=5, to=30, orient=tk.HORIZONTAL, variable=self.oneCharHeight_var, command=self.update_oneCharHeight_label)
        self.oneCharHeight_scale.grid(row=4, column=1, padx=10, pady=10)
        self.oneCharHeight_label = tk.Label(root, text="Character Height: 18")
        self.oneCharHeight_label.grid(row=4, column=2, padx=10, pady=10)

        tk.Label(root, text="Font Size:").grid(row=5, column=0, padx=10, pady=10)
        self.fontSize_scale = ttk.Scale(root, from_=10, to=50, orient=tk.HORIZONTAL, variable=self.fontSize_var, command=self.update_fontSize_label)
        self.fontSize_scale.grid(row=5, column=1, padx=10, pady=10)
        self.fontSize_label = tk.Label(root, text="Font Size: 30")
        self.fontSize_label.grid(row=5, column=2, padx=10, pady=10)

        tk.Checkbutton(root, text="Remove Background", variable=self.remove_bg_var).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(root, text="Color Mode:").grid(row=7, column=0, padx=10, pady=10)
        self.color_mode_menu = ttk.Combobox(root, textvariable=self.color_mode_var, values=["White", "Keep Original Color"])
        self.color_mode_menu.grid(row=7, column=1, padx=10, pady=10)

        tk.Button(root, text="Generate ASCII Image", command=self.process_file).grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.file_path_var.set(file_path)

    def select_output_folder(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            self.output_path_var.set(output_folder)

    def update_scaleFactor_label(self, event=None):
        value = self.scaleFactor_var.get()
        self.scaleFactor_label.config(text=f"Scale Factor: {value:.2f}")

    def update_oneCharWidth_label(self, event=None):
        value = self.oneCharWidth_var.get()
        self.oneCharWidth_label.config(text=f"Character Width: {value}")

    def update_oneCharHeight_label(self, event=None):
        value = self.oneCharHeight_var.get()
        self.oneCharHeight_label.config(text=f"Character Height: {value}")

    def update_fontSize_label(self, event=None):
        value = self.fontSize_var.get()
        self.fontSize_label.config(text=f"Font Size: {value}")

    def process_file(self):
        start_time = time.time()

        file_path = self.file_path_var.get().strip()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid input image file.")
            return

        output_path = self.output_path_var.get().strip()
        if not output_path or not os.path.isdir(output_path):
            messagebox.showerror("Error", "Please select a valid output folder.")
            return

        scaleFactor = self.scaleFactor_var.get()
        oneCharWidth = self.oneCharWidth_var.get()
        oneCharHeight = self.oneCharHeight_var.get()
        font_size = self.fontSize_var.get()
        remove_bg = self.remove_bg_var.get()
        color_mode = self.color_mode_var.get()

        chars = " .-~:+=*#%@"
        charArray = list(chars)
        charlength = len(charArray)
        interval = charlength / 256

        try:
            im = Image.open(file_path)

            if remove_bg:
                im = remove(im)

            if im.mode != 'RGB':
                im = im.convert('RGB')

            font = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', font_size)

            width, height = im.size
            print(f"Actual resolution: {width} x {height}")
            im = RS.resize_image(im, scaleFactor, oneCharWidth, oneCharHeight)
            width, height = im.size
            print(f"Resized resolution: {width} x {height}")

            output_dir = os.path.join(output_path, "OutputImage")
            os.makedirs(output_dir, exist_ok=True)

            # Ensure output directory exists
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir1 = os.path.join(script_dir, "outputFile")
            if not os.path.exists(output_dir1):
                os.makedirs(output_dir1)

            txt_file_path = os.path.join(output_dir1, "output.txt")
            image_output_path = os.path.join(output_path, "output.png")

            with open(txt_file_path, 'w') as txt_file:
                imageOutput = PM.mapping(im, width, height, font, txt_file, oneCharWidth, oneCharHeight, interval, charArray, color_mode)

            imageOutput.save(image_output_path)
            print(f"Your ASCII image has been saved to {image_output_path}")
            print(f"ASCII text file has been saved to {txt_file_path}")

            print("--- %s seconds ---" % (time.time() - start_time))
            messagebox.showinfo("Success", f"ASCII image saved to {image_output_path}\nText file saved to {txt_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_ascii_generator_app():
    root = tk.Tk()
    app = ASCIIImageGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_ascii_generator_app()