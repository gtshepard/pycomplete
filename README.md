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

## Performance 

The key operation for autocomplete is to be able to find all words with the same prefix. This operation must be efficient.
   
   - a naive to this problem can be implemented using a list and is done is O(N * M) time and O(N) space, where N is the number of words in the list, M is the length of the prefix. this is becuase we have to check M letters for of the words in the list.

PyComplete uses a trie (prefix tree) data structure to suggest words

- a trie reduces the complexity to O(K + J), where K is the number of words with the same prefix, and where J is the length of the longest word with the same prefix
this is becuase once we reach the prefix in the trie we have to construct all the words with the same prefix, and there could be as many as K of them and we have to may have to go J nodes deep. we reconstruct words in depth first manner starting from the end of the given prefix (DFS on graph has a similar runtime O(V + E), where V is number of vertices and E is number of edges) 

PyCompletes trie is also space optimized. Tries in general are M-ary trees. Where M is the number of children.
Which have a space complexity O(M * N) where N  is number of nodes 

a node in a trie needs a slot for every charachter that could be stored in the trie. thus if the number of characters is held constant, we reduce
the space complexity to O(N) where N is the number of nodes. PyCompletes Trie restricts the the number of characters the trie will store to 28. 26 of these characters for lowercase english alphabet plus two additonal characters ```-``` and ```'``` characters to account for words like ```all-knowing``` and ```we're```

thus our trie has a space complexity O(N) where N is the number of nodes. 














