import re
class SimpleEditor:
    def __init__(self, document):
        self.document = document
        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = ""

    def search(self, line):
       pattern = re.compile(r"\b%s\b"%line, re.IGNORECASE)
       if pattern.search(self.document) != None:
           return True 
       else:
           return False 


    def cut(self, i, j):
        # building 3 lists, only need to build one 
        self.paste_text = self.document[i:j]
        self.document = self.document[:i] + self.document[j:]

    def copy(self, i, j):
        self.paste_text = self.document[i:j]
        return self.paste_text
    def paste(self, i):
        self.document = self.document[:i] + self.paste_text + self.document[i:]

    def get_text(self):
        return self.document

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result

import timeit

class EditorBenchmarker:
    new_editor_case = """
from __main__ import SimpleEditor
s = SimpleEditor("{}")"""

    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, 3)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 3)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

    def benchmark(self):
        for case in self.cases:
            print("Evaluating case: {}".format(case))
            new_editor = self.new_editor_case.format(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
text_editor = SimpleEditor("i hope that cookies are here")  
class Tester:
    
    def test_copy(self):
        text_editor.document = "Hello Neeva Peeps!"
        expected = "o Ne"
        result = text_editor.copy(4,8)
        print(result)
        assert expected == result  
    
    def test_cut(self):
        text_editor.document = "Cookies and cream!"
        
 
    def test_paste(self):
        pass
 
    def test_misspell(self):
        pass
 
    def test_get_text(self):
        pass 
    
    def test_search(self):
         text_editor.document = "in the winter its Cold, in the summer its warm."
         word_to_find = "winter"
         has_text = text_editor.search(word_to_find)
         assert has_text
        

if __name__ == "__main__":
   # b = EditorBenchmarker(["hello friends"], 100)
   # b.benchmark()

   #text_editor.search("i hope that cookies")
   tester = Tester()
   tester.test_copy()
   tester.test_search()

   # what about punctuation?
   # clean string, place punctuation back if anything was removed
   
   # Performance or Space 
   # use regular expressions for searching for misspellings?
   #

   # Features to ADD
   # text search KMP