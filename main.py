import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from threading import Thread, Event
from findpeace import Findpeace
from utils import shutdown
import animations

# Global events to control the timer
stop_event = Event()
resume_event = Event()
end_event = Event()
timer_thread = None

def start_timer(root, initial_time):
    remaining_time = initial_time * 60  # Convert minutes to seconds

    # Create the timer window
    timer_window = tk.Toplevel(root)
    timer_window.geometry("800x600")
    timer_window.configure(bg="#282A36")

    timer_label = tk.Label(
        timer_window,
        text="Time Remaining: 00:00",
        font=("Lucida Console", 48),
        fg="#FFFFFF",
        bg="#282A36"
    )
    timer_label.pack(expand=True)

    def update_timer():
        nonlocal remaining_time
        if end_event.is_set():
            timer_window.destroy()  # Close the timer window if ended
            show_time_up_window(root)  # Show the "Time's Up" window
            return

        if not stop_event.is_set():
            if remaining_time > 0:
                minutes, seconds = divmod(remaining_time, 60)
                timer_label.config(text=f"Time Remaining: {minutes:02}:{seconds:02}")
                remaining_time -= 1
                timer_window.after(1000, update_timer)  # Updates the timer every second
            else:
                timer_window.destroy()  # Close the timer window when time is up
                show_time_up_window(root)  # Show the "Time's Up" window
        else:
            resume_event.wait()  # Wait for the resume event to be set

    # Start updating the timer
    update_timer()

    # Control buttons
    stop_button = tk.Button(
        timer_window,
        text="Stop Timer",
        font=("Lucida Console", 20),
        command=lambda: stop_event.set(),  # Stop the timer
        bg="#FF6347",
        fg="#FFFFFF"
    )
    stop_button.pack(pady=10)

    resume_button = tk.Button(
        timer_window,
        text="Resume Timer",
        font=("Lucida Console", 20),
        command=lambda: resume_event.set(),  # Resume the timer
        bg="#4682B4",
        fg="#FFFFFF"
    )
    resume_button.pack(pady=10)

    end_button = tk.Button(
        timer_window,
        text="End Timer",
        font=("Lucida Console", 20),
        command=lambda: end_event.set(),  # End the timer
        bg="#FF4500",
        fg="#FFFFFF"
    )
    end_button.pack(pady=10)

def show_time_up_window(root):
    time_up_window = tk.Toplevel(root)
    time_up_window.geometry("800x600")
    time_up_window.configure(bg="#1E1E2E")

    time_up_label = tk.Label(
        time_up_window,
        text="Your allotted time is up!",
        font=("Lucida Console", 36),
        fg="#FFD700",
        bg="#1E1E2E"
    )
    time_up_label.pack(pady=30)

    shutdown_button = tk.Button(
        time_up_window,
        text="Shutdown PC",
        font=("Lucida Console", 20),
        command=shutdown,  # Call the shutdown function
        bg="#FF4500",
        fg="#FFFFFF"
    )
    shutdown_button.pack(pady=20)

    extend_button = tk.Button(
        time_up_window,
        text="Extend Time",
        font=("Lucida Console", 20),
        command=lambda: extend_time(root, time_up_window),
        bg="#32CD32",
        fg="#FFFFFF"
    )
    extend_button.pack(pady=20)

def extend_time(root, parent_window):
    parent_window.destroy()
    extra_minutes = simpledialog.askinteger("Extend Time", "Enter the number of minutes to add:", minvalue=1, maxvalue=60)
    if extra_minutes:
        stop_event.clear()  # Reset stop event
        resume_event.clear()  # Reset resume event
        end_event.clear()  # Reset end event
        global timer_thread
        if timer_thread and timer_thread.is_alive():
            timer_thread.join()  # Wait for the current timer thread to finish
        timer_thread = Thread(target=start_timer, args=(root, extra_minutes))
        timer_thread.start()  # Start the timer in a new thread

def home_screen():
    root = tk.Tk()
    root.geometry("1024x768")
    root.title("DIGITAL GUARD - Find Your Peace")
    root.configure(bg="#101020")

    # Add a background image
    bg_image = Image.open("images/home_bg.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    start_button = tk.Button(
        root,
        text="Start Session",
        font=("Lucida Console", 30),
        command=lambda: start_session(root),
        bg="#483D8B",
        fg="#FFFFFF"
    )
    start_button.pack(expand=True)

    root.mainloop()

def start_session(root):
    try:
        initial_time = Findpeace(root)  # Get the time from the Findpeace function
        if initial_time:  # Check if the time was properly received
            global timer_thread
            if timer_thread and timer_thread.is_alive():
                timer_thread.join()  # Wait for the current timer thread to finish
            timer_thread = Thread(target=start_timer, args=(root, initial_time))
            timer_thread.start()  # Start the timer in a new thread
        else:
            messagebox.showwarning("Input Error", "Failed to retrieve a valid time from Findpeace.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    home_screen()
