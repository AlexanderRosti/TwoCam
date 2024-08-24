import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageStretcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Diamond Image Stretcher")

        # Variables to hold images and corner points
        self.image1 = None
        self.image2 = None
        self.corners1 = None
        self.corners2 = None

        # Predefined target rectangle dimensions
        self.target_width = 300
        self.target_height = 400

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Button to capture images
        btn_capture_images = tk.Button(self.root, text='Capture Images', command=self.capture_images)
        btn_capture_images.pack(pady=10)

        # Button to stretch images
        btn_stretch_images = tk.Button(self.root, text='Stretch Images', command=self.stretch_images)
        btn_stretch_images.pack(pady=10)

        # Canvas for displaying the images
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def capture_images(self):
        # Capture images from cameras
        cap1 = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)

        if not cap1.isOpened() or not cap2.isOpened():
            messagebox.showerror('Camera Error', 'Could not open camera(s).')
            return

        # Capture image from camera 1
        ret1, frame1 = cap1.read()
        if ret1:
            self.image1 = frame1
            self.corners1 = [(50, 50), (frame1.shape[1] - 50, 50), 
                             (50, frame1.shape[0] - 50), (frame1.shape[1] - 50, frame1.shape[0] - 50)]
            self.mark_image_corners(self.image1, '1')

        # Capture image from camera 2
        ret2, frame2 = cap2.read()
        if ret2:
            self.image2 = frame2
            self.corners2 = [(50, 50), (frame2.shape[1] - 50, 50), 
                             (50, frame2.shape[0] - 50), (frame2.shape[1] - 50, frame2.shape[0] - 50)]
            self.mark_image_corners(self.image2, '2')

        cap1.release()
        cap2.release()

    def mark_image_corners(self, image, camera):
        # Mark corners A, B, C, D on the image
        corners = [{'position': (50, 50), 'label': 'A'}, 
                   {'position': (image.shape[1]-50, 50), 'label': 'B'}, 
                   {'position': (50, image.shape[0]-50), 'label': 'C'}, 
                   {'position': (image.shape[1]-50, image.shape[0]-50), 'label': 'D'}]

        for corner in corners:
            cv2.putText(image, corner['label'], corner['position'], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        self.display_image(image, camera)

    def display_image(self, image, camera):
        # Convert image to RGB and display it
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        x = 400 if camera == '1' else 600
        self.canvas.create_image(x, 300, image=image_tk)
        self.root.mainloop()  # Update the mainloop to reflect the changes

    def stretch_images(self):
        # Stretch images based on marked corners
        if self.image1 is None or self.image2 is None:
            messagebox.showwarning('Warning', 'You must capture both images first.')
            return

        # Define source and destination points
        src_points1 = np.float32(self.corners1)
        dst_points1 = np.float32([(0, 0), (self.target_width, 0), 
                                   (0, self.target_height), (self.target_width, self.target_height)])
        src_points2 = np.float32(self.corners2)
        dst_points2 = np.float32([(0, 0), (self.target_width, 0), 
                                   (0, self.target_height), (self.target_width, self.target_height)])

        # Apply perspective transform to stretch images
        matrix1 = cv2.getPerspectiveTransform(src_points1, dst_points1)
        matrix2 = cv2.getPerspectiveTransform(src_points2, dst_points2)

        stretched_image1 = cv2.warpPerspective(self.image1, matrix1, (self.target_width, self.target_height))
        stretched_image2 = cv2.warpPerspective(self.image2, matrix2, (self.target_width, self.target_height))

        # Display the stretched images
        self.display_stretched_images(stretched_image1, stretched_image2)

    def display_stretched_images(self, img1, img2):
        # Convert and display the stretched images
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        img1_pil = Image.fromarray(img1_rgb)
        img2_pil = Image.fromarray(img2_rgb)

        img1_tk = ImageTk.PhotoImage(img1_pil)
        img2_tk = ImageTk.PhotoImage(img2_pil)

        self.canvas.create_image(200, 300, image=img1_tk)
        self.canvas.create_image(600, 300, image=img2_tk)
        self.root.mainloop()  # Update the mainloop to reflect the changes

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageStretcher(root)
    root.mainloop()