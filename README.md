### PyComplete 

PyComplete is a python package for auto complete.
Anyone can include PyComplete in there software to add autcomplete to there software. 

make sure the PyComplete files ```pycomplete.py``` and ```topktrie.py``` files are in the same directory as your main project files

```python 
import pycomplete
```

PyComplete attempts to complete the word that is being typed by looking at the existing prefix and how frequenlty words of this 
prefix have been recorded
```
  Example: 
    if you type 'wh'
    
    
    then PyComplete may suggest: what, when, who 


   However if you type the word whirlpool a ton and what fairly often , and PyComplete is set to suggest up to 3 words
   
   then pycomplete may suggest: 
      whirlpool, what, when
             or 
      whirlpool, what, who
      
   PyComplete will always suggest words in order of most to least frequency. 

```
PyComplete by default remembers the 1000 most frequent words the user types
this value can be changed, however if value is too large, PyComplete may take a performance hit


The PyComplete interface 

```python 
  # make pycomplete remember a word
  def record_word(words: str) -> Void:
  
  # the top k most frequent words with a given prefix
  def suggest_words(prefix: str, k: int) -> []:
```
The user of PyComplete has the freedom to decide how to use pycomplete in there program 


PyComplete uses a trie (prefix tree) data structure suggest words.

the key operations the trie enables us to perform effienctly are word lookup and the task of assembling 

a naive approach for finding all strings with a given prefix useses a list and done is O(n * m) time and O(n) space , where n is the number of words in the list, m is the length of the prefix. this is becuase we have to check m letters for each word in the list.






