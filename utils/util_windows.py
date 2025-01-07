def center_window(window, app_width, app_height):
    """
    Centers a window on the screen based on the given application dimensions.
    
    Args:
        window: The window to center (Tkinter window object).
        app_width (int): The width of the application window.
        app_height (int): The height of the application window.

    Returns:
        str: A geometry string to set the window's size and position.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    return window.geometry(f"{app_width}x{app_height}+{x}+{y}")