from PIL import Image, ImageTk

def load_image(path, size):
    """
    Loads an image from the given path, resizes it to the specified size, 
    and converts it to a PhotoImage object for Tkinter.

    Args:
        path (str): The file path to the image.
        size (tuple): A tuple specifying the width and height for resizing (width, height).

    Returns:
        ImageTk.PhotoImage: A Tkinter-compatible PhotoImage object.
    """
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))
