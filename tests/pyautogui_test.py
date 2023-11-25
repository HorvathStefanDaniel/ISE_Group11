import pyautogui
import subprocess
import time
import os, sys

# Absolute path to the directory containing your image files
script_dir = os.path.dirname(os.path.abspath(__file__))
how_to_play_button_path = os.path.join(script_dir, 'how_to_play_button.jpg')
next_button_path = os.path.join(script_dir, 'next_button_1.png')
main_menu_button_path = os.path.join(script_dir, 'main_menu_button.png')
quit_button_path = os.path.join(script_dir, 'quit_button.png')

# Function to safely perform a click action using PyAutoGUI with image recognition
def click_button(image_filename, confidence=0.8):
    location = pyautogui.locateCenterOnScreen(image_filename, confidence=confidence)
    if location is not None:
        pyautogui.click(location)
    else:
        raise Exception(f"Could not find the {image_filename} on the screen.")

# Function to start the main application and interact with it
def test_main_application():
    print("Starting the application...")
    # Get the path to the Python executable within the virtual environment
    python_executable = sys.executable

    # Start the main.py Tkinter application using the executable
    proc = subprocess.Popen([sys.executable, 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    time.sleep(2)

    try:
        print("Attempting to click 'HOW TO PLAY' button...")
        click_button(how_to_play_button_path)
        print("Clicked on 'HOW TO PLAY'.")
        time.sleep(1)
        click_button(next_button_path)  # Make sure you have a screenshot of this button
        time.sleep(1)  # Wait for the How To Play window to open

        click_button(main_menu_button_path)  # Make sure you have a screenshot of this button
        time.sleep(1)  # Wait for the How To Play window to open
        
        # Perform additional actions here if necessary
        
        # Click on 'QUIT' button or close the application window
        click_button(quit_button_path)  # Make sure you have a screenshot of this button
    except Exception as e:
        print(e)
    finally:
        # Ensure the application is closed at the end of the test
        proc.terminate()  # Terminate the application if it's still running

if __name__ == '__main__':
    test_main_application()
