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

## Performance Tradeoffs

#### Suggest Words Operation 

The key operation for autocomplete is to be able to find all words with the same prefix. This operation must be efficient.
   
   - a naive to this problem can be implemented using a list and is done is O(N * M) time and O(N) space, where N is the number of words in the list, M is the length of the prefix. this is becuase we have to check M letters for of the words in the list.

PyComplete uses a trie (prefix tree) data structure to suggest words

  - a trie reduces the complexity to O(P + J), where P is the number of words with the same prefix, and where J is the number of nodes (eahc node holds a character in a word)needed to form K
  
this is becuase once we reach the prefix in the trie we have to construct all the words with the same prefix, and there could be as many as K of them and we have to may have to go J nodes deep. we reconstruct words in depth first manner starting from the end of the given prefix (DFS on graph has a similar runtime O(V + E), where V is number of vertices and E is number of edges) 

PyCompletes trie is also space optimized. Tries in general are M-ary trees. Where M is the number of children.
Which have a space complexity O(M * N) where N  is number of nodes 

a node in a trie has a child pointer for every charachter that could be stored in the trie. thus if the number of characters is held constant, we reduce
the space complexity to O(N) where N is the number of nodes. PyCompletes Trie restricts the the number of characters the trie will store to 28. 26 of these characters for lowercase english alphabet plus two additonal characters ```-``` and ```'``` characters to account for words like ```all-knowing``` and ```we're```

thus our trie has a space complexity O(N) where N is the number of nodes. 


PyComplete not only suggests words based on prefix, but also based on the frequency that words are used. Thus when PyComplete makes a suggestion based on a prefix, it will be the K most freqeunt words with that prefix. 

  - Since this is a core operation of PyComplete and most likely takes place every time a user presses a key. Time Complexity Performance is favored over space compexity.   
  
      - we first find all P words with the same prefix O(P + J) time and then from there we find the K most frequent words. 
  
      - A naive approach would be to sort all P  words, and take the first K words. resulting O(K + P log P)
      
      PyComplete uses a heap data structure to find the k most frequent words with the same prefix. PyComplete sacrificies space to improve runtime.(naive approach uses O(1) space).
      
          - the heap uses O(P) space and is created in O(P) time with heapfiy 
          - we then pop the K most frequent elements. each pop is constant time, but we do so K times. each time we pop an element from the heap,  we must perocolate the max back up to the top, since there are initally P elements in the heap, this reuslts in a runtime of K log P time
          accounting for heapify. O(P + (K log P)), if K is small, which for autocomplete it should be, it is much closer to O(P + log P) which is quite an improvement over the naive solution. 
          - alittle space is sacrifice a little space for a reduction in runtime 
      
       How does PyComplete store the frequency? the frequency of each word is stored at the last char (node) of each word in the Trie. Tries alwasy have some value to denote the end of a word, thus no additional space is used. a frequency of 0 means that the this node does not mark the end of the word.
       
  
       
       
 ### Record Words Operation 
       
       
      How does PyComplete collect the frequency for words? it uses the record_word() operation.  
      
      this operation operates in O(W) time where W is the length of the word being recorded. a likely time this may be called is everytime a user finishes typing a word. we search for the word in the trie O(W) time, and if it is not in the trie we insert (O(W) time) the word into the trie. this operation happens in O(N) time
      if the word is found in the search its frequency. same goes for insert.
      
    
      you may be wondering why PyComplete does not just store the frequency of the word in a map and update it when a word is found in the map. why store the freqencey in the Trie? 
      
      this would be O(1) access time to see if the word exists and to update the frequency. 
      
      this is because PyComplete wants to keep suggest_words as efficient as possible regardless of its value of K. if frequncy was not stored in the trie getting, getting the frwqucny for the top K words, would take O(K) time. and if K is large this is alot of overhead and will take a toll on PyComplete, because suggestions will be made almost everytime a user presses a key. 
      
  
   
  
 ### Avoiding Mistakes and Slow Downs 
 
to keep suggest_words performance stable, PyComplete removes the least frequently used word after the trie reaches it capacity (a parameter set by the user)
this is for a few reasons, it keeps the space consumed by the Trie bay and words that the user rarely record disappear, but more importantly it reduces the number of words in the trie, that is for any given prefix, it has the chance to reduce the number of of words P with the same Prefix. this keeps P from growing excessivly large over (imagine if words were never deleted. becuase as P grows large, it hurts the runtime O(P + K log P) to construct all words with the same prefix. a core operation of PyComplete. 
 
 
Keeping suggest_words perfomance stable, comes with a cost. we sacrifice some performance in regards to the record_word operation. 


this is the cost of finding the Least Frequently Used (LFU) word and deleting it from the trie when it reaches capacity. this means for a user, who is always at or around capacity, every time they record a word the trie must be pruned. 

this changes the cost of insertion which happens when the user records a word that is not in trie. 

insertion itself is O(L) time. but if the trie is at capacity, the trie must undergo a LFU prune, finding the LFU word can be done in is O(W) time (where W is the number of words) and O(W) space. Deletion can be done in O(L) it, where L is the lenght of the word (just like normal insertion) .
thus insertion becomes an O(2L + W) operation. 

an algorithm proposed by Shah, Mitra, and Matani, can accomplish caching and finding the LFU word in O(1) time, this could bring the overall runtime of insertion back to O(L). 










