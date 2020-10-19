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

#### Suggest Words Operation 

The key operation for autocomplete is to be able to find all words with the same prefix. This operation must be efficient.
   
   - a naive to this problem can be implemented using a list and is done is O(N * M) time and O(N) space, where N is the number of words in the list, M is the length of the prefix. this is becuase we have to check M letters for of the words in the list.

PyComplete uses a trie (prefix tree) data structure to suggest words

  - a trie reduces the complexity to O(M + J), where M is the number of words with the same prefix, and where J is the number of nodes (eahc node holds a character in a word)needed to form K
  
this is becuase once we reach the prefix in the trie we have to construct all the words with the same prefix, and there could be as many as K of them and we have to may have to go J nodes deep. we reconstruct words in depth first manner starting from the end of the given prefix (DFS on graph has a similar runtime O(V + E), where V is number of vertices and E is number of edges) 

PyCompletes trie is also space optimized. Tries in general are M-ary trees. Where M is the number of children.
Which have a space complexity O(M * N) where N  is number of nodes 

a node in a trie needs a slot for every charachter that could be stored in the trie. thus if the number of characters is held constant, we reduce
the space complexity to O(N) where N is the number of nodes. PyCompletes Trie restricts the the number of characters the trie will store to 28. 26 of these characters for lowercase english alphabet plus two additonal characters ```-``` and ```'``` characters to account for words like ```all-knowing``` and ```we're```

thus our trie has a space complexity O(N) where N is the number of nodes. 


PyComplete not only suggests words based on prefix, but also based on the frequency that words are used. Thus when PyComplete makes a suggestion based on a prefix, it will be the K most freqeunt words with that prefix. 

  - Since this is a core operation of PyComplete and most likely takes place every time a user presses a key. Time Complexity Performance is favored over space compexity.   
  
      - we first find all M words with the same prefix O(M + J) time and then from there we find the K most frequent words. 
  
          - A naive approach would be to sort all M words, and take the first K words. resulting O(K + M log M)
      
          PyComplete uses a heap data structure to find the k most frequent words with the same prefix.
       
          to get the freqeun
  



we store the frequency of each of word at the last node of the word in the trie. the end_marker, which already exists on a trie. thus we have used no additional space here.



however if our trie grows to large, perfomance can be hindered so precautions must be taken 


 since this operation is the primary operation, we sarcifce a bit on the runtime of record words, to improve suggest words











