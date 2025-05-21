import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import win32gui
import win32con

class CCTVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CCTV Camera App")
        self.root.configure(bg="#1e1e2f")
        self.root.geometry("800x600")
        self.is_camera_on = False
        self.cap = None

        # Video Display Label
        self.label = tk.Label(root, bg="#1e1e2f")
        self.label.pack(pady=20)

        # Button Frame
        button_frame = tk.Frame(root, bg="#1e1e2f")
        button_frame.pack(pady=10)

        # Button styling
        self.btn_style = {
            "font": ("Segoe UI", 12, "bold"),
            "fg": "#ffffff",
            "bg": "#007acc",
            "activebackground": "#005f99",
            "activeforeground": "#ffffff",
            "width": 16,
            "relief": tk.FLAT,
            "bd": 0,
            "cursor": "hand2",
        }

        #Buttons
        self.btn_start = self.create_button(button_frame, "▶ Start Camera", self.start_camera)
        self.btn_stop = self.create_button(button_frame, "⏹ Stop Camera", self.stop_camera)

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, **self.btn_style)
        btn.pack(side=tk.LEFT, padx=8)
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#3399ff"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#007acc"))
        return btn

    def start_camera(self):
        if not self.is_camera_on:
            self.cap = cv2.VideoCapture(0)
            self.is_camera_on = True
            self.update_frame()

    def stop_camera(self):
        if self.is_camera_on:
            self.is_camera_on = False
            if self.cap:
                self.cap.release()
            self.label.config(image='')

    def update_frame(self):
        if self.is_camera_on and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
            self.root.after(10, self.update_frame)

    def minimize_window(self):
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize_window(self):
        hwnd = win32gui.GetForegroundWindow()
        placement = win32gui.GetWindowPlacement(hwnd)
        if placement[1] == win32con.SW_SHOWMAXIMIZED:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def exit_app(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CCTVApp(root)
    root.mainloop()
