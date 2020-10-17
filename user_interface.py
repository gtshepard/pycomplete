import tkinter as tk 

class MenuBar:
    def __init__(self, parent):
        self.font_specs = ("ubuntu", 14)


        menu_bar = tk.Menu(parent.window, font=self.font_specs)
        
        parent.window.config(menu=menu_bar)
        
        file_dropdown = tk.Menu(menu_bar, font=self.font_specs)
        file_dropdown.add_command(label="New File")
        file_dropdown.add_command(label="Open File")
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Save")
        file_dropdown.add_command(label="Save As")

        menu_bar.add_cascade(label="File", menu=file_dropdown)


class PyWord:
    def __init__(self, window):
        self.window = window
        self.window.bind("<Key>", click)
        self.window.title("Give Me A Name - PyWord")
        self.window.geometry("1200x700")
        self.font_specs = ("ubuntu", 18)
        self.set_default_window(self.window)
        self.menu_bar = MenuBar(self)
   


    def set_default_window(self, main_window):
        self.text_arena = tk.Text(main_window, font=self.font_specs)
        self.scroll_bar = tk.Scrollbar(main_window, command=self.text_arena.yview)
        self.text_arena.configure(yscrollcommand="self.scroll.set")
        self.text_arena.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
   
def click(key):
    print("The Key I Pressed Was: ", key.char)
    if key.char == ' ':
        print("space")

if __name__ == '__main__': 
    main_window = tk.Tk()
    py_word = PyWord(main_window)
    main_window.mainloop()
    main_window.title("PyWord")
    
