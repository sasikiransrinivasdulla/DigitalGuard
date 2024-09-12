import tkinter as tk
from tkinter import messagebox
from utils import get_screen_info
import animations

def Findpeace(root):
    """Displays input forms for the user to provide data and calculates the time extension."""
    input_window = tk.Toplevel(root)
    input_window.geometry("400x400")
    input_window.title("Find Your Peace")
    input_window.configure(bg="#282A36")

    # Widgets to gather user input
    age_label = tk.Label(input_window, text="Enter your age:", font=("Lucida Console", 14), bg="#282A36", fg="#FFFFFF")
    age_label.pack(pady=5)
    age_entry = tk.Entry(input_window, font=("Lucida Console", 14))
    age_entry.pack(pady=5)

    eyesight_label = tk.Label(input_window, text="Do you have any eye-related issues? (yes/no):", font=("Lucida Console", 14), bg="#282A36", fg="#FFFFFF")
    eyesight_label.pack(pady=5)
    eyesight_entry = tk.Entry(input_window, font=("Lucida Console", 14))
    eyesight_entry.pack(pady=5)

    mood_label = tk.Label(input_window, text="Rate your mood (0-10):", font=("Lucida Console", 14), bg="#282A36", fg="#FFFFFF")
    mood_label.pack(pady=5)
    mood_entry = tk.Entry(input_window, font=("Lucida Console", 14))
    mood_entry.pack(pady=5)

    activity_label = tk.Label(input_window, text="Will you chill or work? (chill/work):", font=("Lucida Console", 14), bg="#282A36", fg="#FFFFFF")
    activity_label.pack(pady=5)
    activity_entry = tk.Entry(input_window, font=("Lucida Console", 14))
    activity_entry.pack(pady=5)

    final_time = 0  # Initialize final_time with a default value

    def calculate_time():
        nonlocal final_time  # Ensure final_time can be modified inside this function
        try:
            # Collect inputs
            age = int(age_entry.get())
            eyesight = eyesight_entry.get().lower()
            mood_rating = int(mood_entry.get())
            activity_type = activity_entry.get().lower()

            # Screen and brightness info
            screen_size, brightness = get_screen_info()

            # Algorithm to determine the max time allowed
            max_time = 6 * 60  # Maximum 6 hours in minutes
            min_time = 30  # Minimum 30 minutes

            # Adjusting factors based on user inputs
            time_factor = 1.0  # Default multiplier

            if age < 18:
                time_factor *= 0.8
            if eyesight == 'yes':
                time_factor *= 0.7
            if mood_rating < 4:
                time_factor *= 0.6
            if activity_type == 'work':
                time_factor *= 0.9

            # Adjusting for screen brightness and size
            if brightness > 80:
                time_factor *= 0.8
            if screen_size > 24:  # assuming screen size in inches
                time_factor *= 0.85

            # Calculate final time
            final_time = max(min_time, min(max_time, int(max_time * time_factor)))
            print(f"Calculated time: {final_time} minutes")  # Debugging print statement

            # Show the analyzing window
            animations.show_analyzing_screen(root)

            # After analyzing, show the summary of inputs and the calculated time
            show_summary_screen(root, age, eyesight, mood_rating, activity_type, screen_size, brightness, final_time)

            # Close input window
            input_window.destroy()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid inputs!")

    calculate_button = tk.Button(input_window, text="Calculate", command=calculate_time, font=("Lucida Console", 16), bg="#32CD32", fg="#FFFFFF")
    calculate_button.pack(pady=20)

    input_window.wait_window()

    print(f"Final time returned: {final_time}")  # Debugging print statement
    return final_time  # Return the calculated time

def show_summary_screen(root, age, eyesight, mood_rating, activity_type, screen_size, brightness, calculated_time):
    """Displays the summary of user inputs and the calculated time."""
    summary_window = tk.Toplevel(root)
    summary_window.geometry("500x400")
    summary_window.title("Your Session Details")
    summary_window.configure(bg="#282A36")

    # Display entered details and calculated time
    summary_text = f"""
    Age: {age}
    Eye-related issues: {eyesight}
    Mood Rating: {mood_rating}/10
    Activity Type: {activity_type}
    Screen Size: {screen_size} inches
    Brightness: {brightness}%
    
    Calculated Time: {calculated_time} minutes
    """

    summary_label = tk.Label(summary_window, text=summary_text, justify="left", font=("Lucida Console", 12), bg="#282A36", fg="#FFFFFF")
    summary_label.pack(pady=20)

    # Confirmation button to start the timer
    confirm_button = tk.Button(summary_window, text="OK", command=summary_window.destroy, font=("Lucida Console", 16), bg="#4682B4", fg="#FFFFFF")
    confirm_button.pack(pady=20)

    summary_window.wait_window()
