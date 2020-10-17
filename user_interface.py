import tkinter as tk 

class PyWord:
    def __init__(self, window):
        window.title("Give Me A Name - PyWord")
        window.geometry("1200x700")


if __name__ == '__main__':
    main_window = tk.Tk()
    py_word = PyWord(main_window)
    main_window.mainloop()