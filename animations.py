import tkinter as tk
import random

# Function to animate text character by character on a given label
def animate_text(label, text, delay=50):
    label.config(text="")  # Clear any previous text
    idx = 0

    def update_text():
        nonlocal idx
        if idx < len(text):
            label.config(text=label.cget("text") + text[idx])
            idx += 1
            label.after(delay, update_text)  # Schedule the next character to appear
        else:
            return

    update_text()

# Function to show an "Analyzing" screen with animated text and background effects
def show_analyzing_screen(root):
    anim_window = tk.Toplevel(root)
    anim_window.geometry("800x600")
    anim_window.configure(bg="#0F0F0F")
    anim_window.title("Analyzing...")

    info_label = tk.Label(
        anim_window,
        text="Analyzing the best time for you...",
        font=("Lucida Console", 24),
        fg="#00FF00",
        bg="#0F0F0F"
    )
    info_label.pack(pady=50)

    # Animate binary effect in the background
    binary_frame = tk.Frame(anim_window, bg="#0F0F0F")
    binary_frame.pack(fill=tk.BOTH, expand=True)

    binary_label = tk.Label(
        binary_frame,
        text="",
        font=("Lucida Console", 14),
        fg="#00FF00",
        bg="#0F0F0F"
    )
    binary_label.pack()

    def update_binary():
        # Create random binary string effect
        binary_string = ''.join(random.choice("01") for _ in range(80))
        binary_label.config(text=binary_string)
        binary_frame.after(50, update_binary)

    # Start binary background animation
    update_binary()

    # Animate the analyzing text
    animate_text(info_label, "Analyzing the best time for you...", delay=100)

    # Close window after animation
    anim_window.after(5000, anim_window.destroy)  # Keeps the screen for 5 seconds

# Function to animate a background color change
def animate_bg_color(widget, color1, color2, steps=20, delay=50):
    # Calculate RGB differences
    r1, g1, b1 = widget.winfo_rgb(color1)
    r2, g2, b2 = widget.winfo_rgb(color2)

    r_diff = (r2 - r1) / steps
    g_diff = (g2 - g1) / steps
    b_diff = (b2 - b1) / steps

    # Convert back to hex color
    def rgb_to_hex(r, g, b):
        return f'#{int(r >> 8):02x}{int(g >> 8):02x}{int(b >> 8):02x}'

    step = 0

    def update_color():
        nonlocal step
        if step <= steps:
            new_color = rgb_to_hex(r1 + step * r_diff, g1 + step * g_diff, b1 + step * b_diff)
            widget.config(bg=new_color)
            step += 1
            widget.after(delay, update_color)

    update_color()

# Example usage of animate_bg_color with buttons or any widget
def animate_button_click(button):
    original_color = button.cget("bg")
    highlight_color = "#FFD700"

    # Animate to highlight color and back to original color
    animate_bg_color(button, original_color, highlight_color, steps=10, delay=30)
    button.after(300, lambda: animate_bg_color(button, highlight_color, original_color, steps=10, delay=30))
