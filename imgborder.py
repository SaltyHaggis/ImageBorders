import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Variables
        self.images = []
        self.output_directory = ""
        self.jpg_quality = 90  # Default quality
        self.custom_aspect_ratio = ""
        
        # UI Elements
        self.import_button = tk.Button(root, text="Import Photos", command=self.import_images)
        self.import_button.pack()

        self.aspect_label = tk.Label(root, text="Select Aspect Ratio:")
        self.aspect_label.pack()

        self.aspect_ratio_var = tk.StringVar(value="original")
        self.aspect_ratios = ["Original", "1:1", "3:2", "4:3", "Custom"]
        self.aspect_dropdown = tk.OptionMenu(root, self.aspect_ratio_var, *self.aspect_ratios, command=self.on_aspect_ratio_change)
        self.aspect_dropdown.pack()

        self.custom_ratio_label = tk.Label(root, text="Custom Aspect Ratio:")
        self.custom_ratio_label.pack()
        self.custom_ratio_label.pack_forget()  # Initially hidden

        self.aspect_ratio_display = tk.Label(root, text="Current Aspect Ratio: Original")
        self.aspect_ratio_display.pack()

        self.border_label = tk.Label(root, text="Set Border Width (%):")
        self.border_label.pack()
        
        # Border width slider (changed range to 0-25)
        self.border_scale = tk.Scale(root, from_=0, to_=25, orient=tk.HORIZONTAL)
        self.border_scale.pack()

        self.resize_label = tk.Label(root, text="Resize Max Dimension (px):")
        self.resize_label.pack()

        self.max_dimension = tk.Entry(root)
        self.max_dimension.insert(0, "1080")  # Set default value to 1080
        self.max_dimension.pack()

        # Change from dropdown to entry for JPG Quality
        self.jpg_quality_label = tk.Label(root, text="Select JPG Quality (1-100):")
        self.jpg_quality_label.pack()

        self.jpg_quality_input = tk.Entry(root)
        self.jpg_quality_input.insert(0, "90")  # Default value of 90
        self.jpg_quality_input.pack()

        self.export_button = tk.Button(root, text="Export Images", command=self.export_images)
        self.export_button.pack()

    def import_images(self):
        self.images = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.images:
            messagebox.showinfo("Import", f"{len(self.images)} image(s) imported.")

    def export_images(self):
        if not self.images:
            messagebox.showerror("Error", "No images to export.")
            return
        
        # Ask user to select an export folder after pressing "Export"
        self.output_directory = filedialog.askdirectory(title="Select Export Folder")
        if not self.output_directory:
            messagebox.showerror("Error", "Please select an export folder.")
            return
        
        aspect_ratio = self.aspect_ratio_var.get()
        border_width = self.border_scale.get()  # Get the current value of the border width slider
        resize_max = self.max_dimension.get()

        if not resize_max.isdigit():
            messagebox.showerror("Error", "Please enter a valid number for the resize dimension.")
            return
        
        resize_max = int(resize_max)
        
        # Get JPG quality from the input field
        quality_input = self.jpg_quality_input.get()

        # Validate the JPG quality value and auto-correct if needed
        if not quality_input.isdigit() and not (quality_input.startswith('-') and quality_input[1:].isdigit()):
            quality_input = "90"  # Default value if invalid input
        else:
            quality_input = int(quality_input)
            if quality_input < 1:
                quality_input = 1  # Adjust to 1 if input is less than 1 or negative
                self.jpg_quality_input.delete(0, tk.END)
                self.jpg_quality_input.insert(0, str(quality_input))  # Update the input box with the new value
            elif quality_input > 100:
                quality_input = 100  # Adjust to 100 if input is greater than 100
                self.jpg_quality_input.delete(0, tk.END)
                self.jpg_quality_input.insert(0, str(quality_input))  # Update the input box with the new value

        self.jpg_quality = quality_input
        
        # Process each image
        for image_path in self.images:
            try:
                img = Image.open(image_path)
                # Apply aspect ratio with center fitting and border width
                img, border = self.apply_aspect_ratio_with_center(img, aspect_ratio, border_width)
                # Resize image
                img = self.resize_image(img, resize_max)
                # Set export path
                output_path = self.output_directory + "/" + image_path.rsplit('/', 1)[-1].rsplit('.', 1)[0] + "_processed.jpg"
                img.save(output_path, "JPEG", quality=self.jpg_quality)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing image {image_path}: {e}")
                continue

        messagebox.showinfo("Export", "Images exported successfully.")


    def apply_aspect_ratio_with_center(self, img, aspect_ratio, border_width_percentage):
        width, height = img.size
        
        # Calculate border width based on slider percentage
        border_width = int(border_width_percentage / 100 * max(width, height))

        # Initialize the final border size with border applied
        if aspect_ratio == "1:1":
            target_width = target_height = min(width, height)
        elif aspect_ratio == "3:2":
            target_width = width
            target_height = int(width * 2 / 3)
        elif aspect_ratio == "4:3":
            target_width = width
            target_height = int(width * 3 / 4)
        elif aspect_ratio == "Custom":
            # Parse the custom aspect ratio from user input
            custom_ratio = self.custom_aspect_ratio.split(":")
            if len(custom_ratio) != 2:
                return img, None
            try:
                custom_width = int(custom_ratio[0])
                custom_height = int(custom_ratio[1])
                target_width = custom_width * height // custom_height
                target_height = height
            except ValueError:
                return img, None
        else:  # "Original"
            # If original, just add border to the current image size
            target_width = width + 2 * border_width
            target_height = height + 2 * border_width

        # Create the border (expand the canvas to the desired aspect ratio)
        border = Image.new('RGB', (target_width, target_height), color='white')

        # Position the image in the center of the border
        img_aspect_ratio = width / height
        border_aspect_ratio = target_width / target_height

        if img_aspect_ratio > border_aspect_ratio:
            new_width = target_width - (border_width * 2)
            new_height = int(new_width / img_aspect_ratio)
        else:
            new_height = target_height - (border_width * 2)
            new_width = int(new_height * img_aspect_ratio)

        img_resized = img.resize((new_width, new_height))
        
        # Calculate position to center the image inside the border
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2

        # Paste the image in the center of the border
        border.paste(img_resized, (x_offset, y_offset))

        return border, img_resized

    def resize_image(self, img, max_dim):
        width, height = img.size
        aspect_ratio = width / height
        
        if width > height:
            new_width = max_dim
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_dim
            new_width = int(new_height * aspect_ratio)
        
        img = img.resize((new_width, new_height))
        return img

    def on_aspect_ratio_change(self, value):
        """Handle changes in aspect ratio dropdown"""
        if value == "Custom":
            # Show the custom ratio pop-up
            self.show_custom_ratio_popup()
        else:
            # Update the visual cue with the selected aspect ratio
            self.custom_aspect_ratio = ""  # Clear custom aspect ratio
            self.aspect_ratio_display.config(text=f"Current Aspect Ratio: {value}")

    def show_custom_ratio_popup(self):
        """Show the custom aspect ratio input pop-up"""
        popup = tk.Toplevel(self.root)
        popup.title("Enter Custom Aspect Ratio")

        # Label and Entry widgets for width and height
        tk.Label(popup, text="Width:").pack()
        width_entry = tk.Entry(popup)
        width_entry.pack()

        tk.Label(popup, text="Height:").pack()
        height_entry = tk.Entry(popup)
        height_entry.pack()

        def on_ok():
            width = width_entry.get()
            height = height_entry.get()

            if width.isdigit() and height.isdigit():
                self.custom_aspect_ratio = f"{width}:{height}"
                self.aspect_ratio_display.config(text=f"Current Aspect Ratio: {self.custom_aspect_ratio}")
                popup.destroy()
            else:
                messagebox.showerror("Error", "Please enter valid numbers for width and height.")

        ok_button = tk.Button(popup, text="OK", command=on_ok)
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
