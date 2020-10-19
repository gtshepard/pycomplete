### PyComplete 

PyComplete is a python package for AutoComplete.
Anyone can include PyXomplete in there software to add autcomplete to there software. 

make sure the PyComplete files pycomplete.py and topktrie.py files are in the same directory as you main project files
```python 
import pycomplete
```

PyComplete attempts to complete the word that is being typed by looking at the existing prefix. 
```
  Example: 
    if you type 'wh'

    PyComplete may suggest: what, when, who 

```

PyComplete suggests words based on two conditions. the prefix that is being typed and the frequency that the user
types these words. PyComplete's default to ensure fast word suggestion is to rememeber the 1000 most frequent words the user types
this value can be changed, however if value is too large, one may take a performance hit


The PyComplete interface 
```python 
  # make pycomplete remember a word
  def record_word(words: str) -> Void:
  
  # the top k most frequent words with a given prefix
  def suggest_words(prefix: str, k: int) -> []:
```
The user of PyComplete has the freedom to decide how to use pycomplete in there program 
PyComplete
