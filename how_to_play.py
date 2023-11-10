# how_to_play.py

import tkinter as tk

class HowToPlay:
    def __init__(self, root, images, on_main_menu):
        self.root = root
        self.images = images
        self.on_main_menu = on_main_menu
        self.index = 0
        
        # Setting up the UI elements
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack()

        # Show the first image
        self.show_image(self.index)

    def show_image(self, index):
        image = self.images[index]
        photo = tk.PhotoImage(file=image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # keep a reference!

        # If it's the last image, change button text to "Main Menu"
        if index == len(self.images) - 1:
            self.next_button.config(text="Main Menu")

    def next_image(self):
        self.index += 1

        if self.index < len(self.images):
            self.show_image(self.index)
        else:
            self.on_main_menu()  # Call the passed in function to show the main menu
