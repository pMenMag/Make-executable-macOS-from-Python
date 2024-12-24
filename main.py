import PySimpleGUI as sg
from PIL import Image, ImageTk
import os
import random

def resize_image(image_path, window_size):
    """
    Resize the image to fit the window size, preserving aspect ratio.
    """
    max_width, max_height = window_size
    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height))  # Resize the image
        return ImageTk.PhotoImage(img)

def get_random_image_from_fixed_folder(folder_path):
    """
    Get a random image file from the specified folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))]

    if not image_files:
        raise FileNotFoundError(f"No image files found in the folder '{folder_path}'.")

    return os.path.join(folder_path, random.choice(image_files))

def create_image_widget():
    sg.theme("LightBlue")  # Set the GUI theme

    # Fixed folder for random images
    fixed_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")  # Replace with your folder path

    # Start with a random image
    initial_image_path = None
    try:
        initial_image_path = get_random_image_from_fixed_folder(fixed_folder)
    except Exception as e:
        sg.popup_error(f"Error loading initial random image: {e}")

    # Window layout
    layout = [
        [sg.Text("Welcome to the Bebsis Generator!", font=("Helvetica", 14), justification="center")],
        #[sg.Input(key="-FILE-", enable_events=True, visible=False),
        # sg.FileBrowse("Browse", file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),))],
        [sg.Image(key="-IMAGE-", size=(400, 400))],  # Placeholder for the image
        [sg.Button("I Want a Knew Bebsi!", size=(20, 2))]
    ]

    # Create the window
    window = sg.Window("Hallo, Bebi!", layout, finalize=True, element_justification="center", resizable=True)

    # Load and display the initial random image after the window is created
    try:
        initial_image_path = get_random_image_from_fixed_folder(fixed_folder)
        img = resize_image(initial_image_path, window_size=(400, 400))
        window["-IMAGE-"].update(data=img)
    except Exception as e:
        sg.popup_error(f"Error loading initial random image: {e}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        # File selected
        if event == "-FILE-":
            file_path = values["-FILE-"]

            if os.path.exists(file_path):
                try:
                    # Resize and load image
                    img = resize_image(file_path, window_size=(400, 400))
                    window["-IMAGE-"].update(data=img)
                except Exception as e:
                    sg.popup_error(f"Error loading image: {e}")

        # Show random image
        if event == "I Want a Knew Bebsi!":
            try:
                random_image_path = get_random_image_from_fixed_folder(fixed_folder)
                img = resize_image(random_image_path, window_size=(400, 400))
                window["-IMAGE-"].update(data=img)
            except Exception as e:
                sg.popup_error(f"Error showing random image: {e}")

    window.close()

# Run the widget
if __name__ == "__main__":
    create_image_widget()
