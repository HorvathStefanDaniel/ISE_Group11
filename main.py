# main.py
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk  # For adding images
from how_to_play import HowToPlay
from initDb import init_db
from edit_questions import edit_questions_window
from play_game import play_game_window  # make sure to import the play_game_window function


# Define a larger font for the buttons
button_font = ('Arial', 20, 'bold')

DATABASE = 'quiz_game.db'

##### FOR TESTING #####

def execute_db_query(query, parameters=(), fetchall=False, commit=False):
    """
    Execute a database query.

    :param query: SQL query string.
    :param parameters: Tuple of parameters for the SQL query.
    :param fetchall: If True, fetches all rows from the query result.
    :param commit: If True, commits the transaction.
    :return: Query result if fetchall is True or lastrowid if commit is True.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        if commit:
            conn.commit()
            return cursor.lastrowid
        if fetchall:
            return cursor.fetchall()
        return cursor.fetchone()

# Example usage of execute_db_query
def load_topics_from_db():
    """
    Load topics from the database.
    
    :return: List of topic tuples.
    """
    return execute_db_query("SELECT * FROM Topics", fetchall=True)

##### END FOR TESTING #####

def create_rounded_button(canvas, x, y, width, height, corner_radius, text, command):
    # Create a rounded rectangle
    canvas.create_oval(x, y, x + 2 * corner_radius, y + 2 * corner_radius, fill='white', outline='')
    canvas.create_oval(x + width - 2 * corner_radius, y, x + width, y + 2 * corner_radius, fill='white', outline='')
    canvas.create_oval(x, y + height - 2 * corner_radius, x + 2 * corner_radius, y + height, fill='white', outline='')
    canvas.create_oval(x + width - 2 * corner_radius, y + height - 2 * corner_radius, x + width, y + height, fill='white', outline='')
    canvas.create_rectangle(x + corner_radius, y, x + width - corner_radius, y + height, fill='white', outline='')
    canvas.create_rectangle(x, y + corner_radius, x + width, y + height - corner_radius, fill='white', outline='')
    
    # Add text to the button
    canvas.create_text(x + width / 2, y + height / 2, text=text, font=('Arial', 20, 'bold'))
    
    # Bind the click event
    canvas.tag_bind("button", "<Button-1>", lambda event: command())

def get_tiled_background_segment(bg_image_path, segment_size, offset=(0, 0)):
    # Ensure to use the global variables
    global bg_width, bg_height
    # Load and tile the background image
    background_image = Image.open(bg_image_path)
    tiled_bg = Image.new('RGB', segment_size)

    for x in range(-offset[0], segment_size[0], bg_width):
        for y in range(-offset[1], segment_size[1], bg_height):
            tiled_bg.paste(background_image, (x, y))

    return tiled_bg

def show_main_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    set_background_image()  # Set the background image
    # Recreate the main menu
    create_main_menu()

def edit_questions():
    edit_window = edit_questions_window(root)

def set_background_image():
    global bg_width, bg_height
    # Load the background image
    background_image = Image.open('background.png')  # Replace 'background.png' with your actual file path
    bg_width, bg_height = background_image.size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Create a new image for the tiled background
    tiled_bg = Image.new('RGB', (screen_width, screen_height))
    
    for x in range(0, screen_width, bg_width):
        for y in range(0, screen_height, bg_height):
            tiled_bg.paste(background_image, (x, y))

    tk_tiled_bg = ImageTk.PhotoImage(tiled_bg)

    # Create a label that will contain the tiled background
    background_label = tk.Label(root, image=tk_tiled_bg)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = tk_tiled_bg  # Keep a reference

def create_main_menu():
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    ############## LOGO ##############

    # Calculate the size of the logo (10% of the screen or 50x50 pixels, whichever is smaller)
    logo_size = min(200, screen_width // 5, screen_height // 5)

    # Calculate the position to center the logo on the screen
    logo_x = (screen_width - logo_size) // 2
    logo_y = (screen_height - logo_size) // 10  # Adjust vertical position as needed

    # Open the logo with PIL and ensure it has an alpha layer
    original_logo = Image.open('quizLogo.png').convert("RGBA")
    resized_logo = original_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Get a segment of the tiled background that matches the logo size with the correct offset
    bg_segment = get_tiled_background_segment('background.png', (logo_size, logo_size), (logo_x % bg_width, logo_y % bg_height))

    # Composite the vignette logo over the background segment
    combined_logo = Image.alpha_composite(bg_segment.convert("RGBA"), resized_logo)

    # Convert to a format suitable for Tkinter
    logo = ImageTk.PhotoImage(combined_logo)

    # Create a Canvas for the logo with a transparent background
    logo_canvas = tk.Canvas(root, width=logo_size, height=logo_size, bg='green', highlightthickness=0, borderwidth=0)
    logo_canvas.create_image((logo_size // 2, logo_size // 2), image=logo)
    logo_canvas.image = logo  # Keep a reference so it's not garbage collected
    logo_canvas.pack(pady=20)


    ############## BUTTONS ##############

    # Get a segment of the tiled background that matches the size needed for the button frame
    button_frame_width = screen_width  # Adjust the width as needed
    button_frame_height = 300  # Adjust the height as needed, enough to contain all buttons
    bg_segment = get_tiled_background_segment('background.png', (button_frame_width, button_frame_height))

    # Convert to a format suitable for Tkinter
    button_bg = ImageTk.PhotoImage(bg_segment)

    # Create a Canvas for the buttons with the tiled background
    button_canvas = tk.Canvas(root, width=button_frame_width, height=button_frame_height, highlightthickness=0)
    button_canvas.create_image((button_frame_width // 2, button_frame_height // 2), image=button_bg)
    button_canvas.image = button_bg  # Keep a reference so it's not garbage collected
    button_canvas.pack(pady=20)

    # Define the button width and height
    button_width = 300  # Adjust to your preferred width
    button_height = 50  # Adjust to your preferred height

    # Create the buttons and use the `create_window` method to place them on the canvas
    play_button = tk.Button(root, text="PLAY", command=show_game, font=button_font)
    button_canvas.create_window((button_frame_width // 2, 50), window=play_button, width=button_width, height=button_height)

    edit_questions_button = tk.Button(root, text="EDIT QUESTIONS", command=edit_questions, font=button_font)
    button_canvas.create_window((button_frame_width // 2, 120), window=edit_questions_button, width=button_width, height=button_height)

    how_to_play_button = tk.Button(root, text="HOW TO PLAY", command=show_how_to_play, font=button_font)
    button_canvas.create_window((button_frame_width // 2, 190), window=how_to_play_button, width=button_width, height=button_height)

    quit_button = tk.Button(root, text="QUIT", command=root.quit, font=button_font)
    button_canvas.create_window((button_frame_width // 2, 260), window=quit_button, width=button_width, height=button_height)


def show_how_to_play():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Images for how to play
    images = ["KeyboardPlayers.png", "KeyboardSelectAnswer.png"]  # replace with your actual image paths

    # Create the How to Play page
    HowToPlay(root, images, show_main_menu)

def show_game():
    # Clear the window or hide the current window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Start the game and pass the function to return to main menu after game ends
    play_game_window(root, show_main_menu, DATABASE)

root = tk.Tk()

# Make the window full screen
root.attributes('-fullscreen', True)
# Or you can use this for a maximized window, which may be more user-friendly:
# root.state('zoomed')

set_background_image()  # Set the background image
create_main_menu()  # Start with the main menu

# Call the init_db function to initialize the database at startup
init_db(DATABASE) #name of the database is quiz_game.db

root.mainloop()
