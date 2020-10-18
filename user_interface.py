import tkinter as tk 
from tkinter import filedialog
class MenuBar:
    def __init__(self, parent):
        self.font_specs = ("ubuntu", 14)


        menu_bar = tk.Menu(parent.window, font=self.font_specs)
        
        parent.window.config(menu=menu_bar)
        
        file_dropdown = tk.Menu(menu_bar, font=self.font_specs)
        file_dropdown.add_command(label="New File",accelerator="Ctrl+N", command=parent.new_file)
        file_dropdown.add_command(label="Open File", accelerator="Ctrl+O",command=parent.open_file)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Save", accelerator="Ctrl+S", command=parent.save)
        file_dropdown.add_command(label="Save As",
                                  accelerator="Ctrl+Shift+S",
                                  command=parent.save_as)

        menu_bar.add_cascade(label="File", menu=file_dropdown)



class PyWord:
    def __init__(self, window):
        # sets up intial program window 
        self.window = window
        self.window.bind("<Key>", self.on_user_type)
        #self.window.title("Give Me A Name - PyWord")
        self.window.geometry("1200x700")
        self.font_specs = ("ubuntu", 18)
        self.set_default_window(self.window)
        self.menu_bar = MenuBar(self)
        # this is auto complete window may be a better way to do this like press tab to autocomplete
        # no buttons needed 
        self.canvas = tk.Canvas(self.window, bg="blue", width=300, height=300)
        self.canvas.pack(fill="both", side="right", expand=True)
        self.words = ['cat', 'dog', 'bear', 'frog', 'bird']
        self.y_position_for_word = 10
        self.text_ids = {}
        self.char_count = 0

        self.filename = None 
        self.bind_keyboard_shortcuts()

    # sets adds features to main window 
    def set_default_window(self, main_window):
        self.text_arena = tk.Text(main_window, font=self.font_specs)
        self.scroll_bar = tk.Scrollbar(main_window, command=self.text_arena.yview)
        self.text_arena.configure(yscrollcommand="self.scroll.set")
        self.text_arena.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # detect user typing, keep a character count so we know the last index 
    # of the word. 
    def on_user_type(self, key):
        print("The Key I Pressed Was: ", key.char)
        self.clear_words()
        #keep track whe
        if key.char != '\x7f':
            self.char_count += 1
        else:
            if self.char_count > 0:
                self.char_count -= 1
        
        # right now not hooked up to autocomplete so ignore 
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

    # this will grab from autocomplete
    def get_words(self):
        return self.words

    # clears words from canvas will be useful later 
    def clear_words(self):
         for t, _ in self.text_ids.items():
            self.canvas.delete(t)
            self.text_ids = {}
            self.y_position_for_word = 10
         self.canvas.update()

    # when i hit the space key autocomplete window should close 
    # when im am typing other characters auto complete winodw
    # should be opening and recommend top 3 words 
    def set_window_title(self, name=None):
        # 2 cases 
        if name:
            self.window.title(name + "- PyWord")
        else:
            self.window.title("unititled - PyWord")


    def new_file(self, *args):
        self.text_arena.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension = ".txt", 
            filetypes = [("All Files", "*.*"),
                         ("Text Files", "*.txt"),
                         ("Python Scripts", "*.py"),
                         ("Markdown Document", "*.md")
                         ]
            )

        if self.filename:
            self.text_arena.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.text_arena.insert(1.0, f.read())
            self.set_window_title(self.filename)

    def save(self, *args):
        if self.filename:
            try:
                text_content = self.text_arena.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(text_content)
                
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self,*args):
        print("save_as Called")
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                           ("Text Files", "*.txt"),
                           ("Python Scripts", "*.py"),
                           ("Markdown Documents", "*.md"),
                           ("JavaScript Files", "*.js"),
                           ("HTML Documents", "*.html"),
                           ("CSS Documents", "*.css")])
            textarea_content = self.text_arena.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)

        except Exception as e:
            print(e)

    def bind_keyboard_shortcuts(self):
        self.text_arena.bind('<Control-n>', self.new_file)
        self.text_arena.bind('<Control-o>', self.open_file)
        self.text_arena.bind('<Control-s>', self.save)
        self.text_arena.bind('<Control-S>', self.save_as)
# reccomends word on panel to side 
# the 1 key reccomends first word, 2 key reccomends 2nd word and so on
if __name__ == '__main__': 
    main_window = tk.Tk()
    py_word = PyWord(main_window)
    main_window.mainloop()
    main_window.title("PyWord")
 