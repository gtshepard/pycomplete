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
        self.window.bind("<Key>", self.on_user_type)
        self.window.title("Give Me A Name - PyWord")
        self.window.geometry("1200x700")
        self.font_specs = ("ubuntu", 18)
        self.set_default_window(self.window)
        self.menu_bar = MenuBar(self)
        #self.auto_suggest_window = AutoSuggestWindow()
        self.canvas = tk.Canvas(self.window, bg="blue", width=300, height=300)
        self.canvas.pack(fill="both", side="right", expand=True)
        #self.canvas.create_text(10,10,text="Hello world!", anchor="nw")
        #self.canvas.create_text(10,100,text="This is the end of the  words!", anchor="nw")
        #self.canvas.update()
        self.words = ['cat', 'dog', 'bear', 'frog', 'bird']
        self.y_position_for_word = 10
        self.text_ids = {}
        self.char_count = 0

    def set_default_window(self, main_window):
        self.text_arena = tk.Text(main_window, font=self.font_specs)
        self.scroll_bar = tk.Scrollbar(main_window, command=self.text_arena.yview)
        self.text_arena.configure(yscrollcommand="self.scroll.set")
        self.text_arena.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
   
    def on_user_type(self, key):
        print("The Key I Pressed Was: ", key.char)
    
        
        self.clear_words()
        #keep track whe
        if key.char != '\x7f':
            self.char_count += 1
        else:
            if self.char_count > 0:
                self.char_count -= 1
        # add a new set of if not space
        if key.char != ' ':
            words = self.get_words()
            for w in words:
                text_key = self.canvas.create_text(10, self.y_position_for_word,text=w, font="Arial 24 bold", anchor="nw")
                self.text_ids[text_key] = text_key
                self.y_position_for_word += 24
            self.canvas.update()
    
    def copy(self):
        print("Button Click")
        #self.text_arena.insert(self.char_count)
        #button1.text 

    def get_words(self):
        return self.words

    def clear_words(self):
         for t, _ in self.text_ids.items():
            self.canvas.delete(t)
            self.text_ids = {}
            self.y_position_for_word = 10
         self.canvas.update()

    # when i hit the space key autocomplete window should close 
    # when im am typing other characters auto complete winodw
    # should be opening and recommend top 3 words 

if __name__ == '__main__': 
    main_window = tk.Tk()
    py_word = PyWord(main_window)
    main_window.mainloop()
    main_window.title("PyWord")
