import tkinter as tk
from ui import TuringTestApp
from logic import CaptchaLogic

if __name__ == "__main__":
    root = tk.Tk()
    captchaLogic = CaptchaLogic()
    app = TuringTestApp(root, captchaLogic)
    root.mainloop()
