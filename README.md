# Neeva Software Engineer, New Grad 2021, Text Editor Project -  Interview Stage 1 - Garrison Shepard

## PyComplete an Autocomplete Library 

1. [Overview](#overview)
2. [How To Run This Project](#how-to-run-this-project)
3. [Understanding The Performance](#understanding-the-performance)
   1. [Autocomplete](#autocomplete)
   2. [K Most Frequent Words](#k-most-frequent-words)
   3. [Least Frequently Used Pruning](#least-frequently-used-pruning)
   4. [Room For Improvement](#room-for-improvement)

### Overview 

I chose to work on the text editor project as it best suits my interests and skill set. The project allowed for creative freedom. I chose to focus on adding additional features to the text editor and optimizing the features that I did add. 

I built an autocomplete library for the text editor called PyComplete. 

PyComplete suggests the  ```K``` most frequent words for a given prefix. PyComplete records  input words and adjusts their frequencies. When a prefix is given as input, the ```K``` most frequent words with that prefix are suggested. 

Suppose ```K = 3``` and one  records the words ``` what``` 10 times, ```when``` 4 times, ```who``` 2 times, and ```whale``` 1 time. Then the prefix ```wh``` is given as input. 

PyComplete would suggest: ````what, when, who````. 

PyComplete by default remembers the 1000 most frequent words the user type. This is a parameter that the user can change. 

The PyComplete interface 

```python 
  # record word and update frequency 
  def record_word(words: str) -> Void:
  
  # the top k most frequent words with a given prefix
  def suggest_words(prefix: str, k: int) -> []:
```

## How To Run This Project

 - Make sure python3 and pip3 are installed 
 - to install required dependencies type
 ``` pip3 install -r requirements.txt ```
 - for a quick demo run 
 ```Python autocomplete.py```
 - To run test cases 
 ```Pytest test_autocomplete.py ```
 - to use PyComplete in a project
 
```python
   import autocomplete.py
   import topktie.py
```
 
## Understanding The Performance 

### Autocomplete 

The key operation for autocomplete is to be able to retrieve all ```P``` words with the same prefix. This operation must be efficient.

a naive to this problem can be implemented using a list and is done is ```O(N * M)``` time and O(N) space, where N is the number of words in the list, M is the length of the prefix. This is because we have to check M letters for each word in the list.

PyComplete uses a Trie (prefix tree) data structure to suggest words

a Trie reduces the complexity to ```O(P + J)```, where ```P``` is the number of words with the same prefix, and where J is the number of nodes needed to form ```P``` words
  
this is because once we reach the prefix in the Trie we have to construct all the words with the same prefix, and there could be as many as ```P``` of them and there may be as many as J nodes to visit to accumulate characters in order to form these``` P``` words. we reconstruct words in depth first manner starting from the end of the given prefix 

PyCompletes Trie is also space optimized.  Tries in general are ```M-ary``` trees. Where ```M``` is the number of children. Which have a space complexity ```O(M * N)``` where ```N```  is number of nodes 

A node in a Trie has a child pointer for every character that could be stored in the trie. thus if the number of characters is held constant, we reduce
the space complexity to ```O(N)``` where ```N``` is the number of nodes. PyCompletes Trie restricts the number of characters the Trie will store to 28. 26 of these characters for lowercase english alphabet plus two additional characters ```-``` and ```'``` characters to account for words like ```all-knowing``` and ```we're```. Thus our Trie has a space complexity ```O(N)``` where ```N``` is the number of nodes, because the width of Trie is constant (28 characters)

### K Most Frequent Words 

PyComplete not only suggests words based on prefix, but also based on the frequency that words are used. Thus when PyComplete makes a suggestion based on a prefix, it will be the ```K``` most frequent words with that prefix. Since this is a core operation of PyComplete and most likely takes place every time a user presses a key. Time Complexity Performance is favored over space compexity.   

we first find all ```P``` words with the same prefix ```O(P + J)``` time and then from there we find the K most frequent words. 

A naive approach to finding the ```K``` most frequent words out of ```P``` words  would be to sort all ```P```  words, and take the first ```K``` words. resulting ```O(K + P log P)```
      
PyComplete uses a heap data structure to find the ```K``` most frequent words with the same prefix. PyComplete sacrifices to improve runtime. (naive approach uses O(1) space). the heap uses ```O(P)``` space and is created in ```O(P)``` time with heapify. We then pop the ```K``` most frequent elements. Each pop is a constant time operation, but we do so ```K``` times. However every time an element is popped, a new max must be percolated to the top, since there are initially ```P``` elements in the heap,, percolate  takes ```O(log P)``` time, this results in a runtime of ```O(K log P)``` time for popping and element and percolating a  new element to the top. If we take into account building  the heap, we have ```O(P + (K log P))```, if ```K``` is small, which for autocomplete it should be, it is much closer to ```O(P + log P)``` which is quite an improvement over the naive solution. alittle space is sacrifice a little space for a reduction in runtime 

How does PyComplete store the frequency? the frequency of each word is stored at the last char (node) of each word in the Trie. Trie’s always have some value to denote the end of a word, thus no additional space is used. a frequency of 0 means that this node does not mark the end of the word.

How does PyComplete collect the frequency for words? it uses the record_word() operation.  

The record_word operation  operates in ```O(L)``` time where ```L``` is the length of the word being recorded. a likely time this may be called is everytime a user finishes typing a word. 

The two operations behind record word are Trie search and Trie insertion both taking O(L) time. If the word is not in the Trie, it is inserted and its frequency is adjusted to 1. If the word already exists, its frequency is adjusted by 1. 
      
you may be wondering why PyComplete does not just store the frequency of the word in a map and update it when a word is found in the map. Why store the freqencey in the Trie? this would be ```O(1)``` access time to see if the word exists and to update the frequency. 

This is because PyComplete wants to keep suggest_words as efficient as possible regardless of its value of ```K```. if frequency was not stored in the trie getting, getting the frequency for the top K words, would take ```O(K)``` time. and if K is large this is a lot of overhead and will take a toll on PyComplete, because autcomplete suggestions will be made almost every time a user presses a key. 
      
To avoid suggesting  misspelled words, before PyComplete records a word, it makes sure it is a valid word by looking it up in the dictionary. 

### Least Frequently Used Pruning
 
To keep performance stable for autocomplete, PyComplete removes the least frequently used word after the Trie reaches it capacity (a parameter set by the user) this is for a few reasons,

This sets a bound on the number of words in the Trie. Which ultimately leads to a more predictable and stable runtime. 

***Why is this important?***

If we have alot of words in the Trie, it is more likely that ```P``` (the number of words with the same prefix) will be a large number.
if ```P``` is large that means our Autcomplete operation's performance suffers. this is becuause all operations for autocomplete rely on the value of ```P```
to get all words from the trie with the same prefix we must spend ```O(P + J)``` time and then to get the ```K``` most freqeunt words from this grouping we must spend ```O(P + K log P)``` time.

if we never removed any words from the Trie ```P``` over time could theoretically become so large that the Autcomplete operation would become unusable. Thus we prune the trie once a set capacity is reached, so ```P``` can never grow large enough to render autocomplete unusable. We remove the Least Frequently Used element so the user is only suggested the most frequent words. if we removed any word, it could be the case we accidentally removed the most frequent word.
 
### Room For Improvement 

Keeping the performance stable came with a cost. The operation that keeps our Trie up to date becomes slower. 

When we prune the Trie to keep it at a set capacity, there is a performance hit to the autocomplete operation. This performance hit comes from  the cost of finding the Least Frequently Used (LFU) word and deleting it from the Trie when it reaches capacity. 

This happens in ```O(L + W)``` time. while one may thin this does not happen often, however it can. For the user who is hovering around capacity almost every time they record a word the Trie must be pruned. This changes the cost of insertion.

insertion takes place whenever a user records a word, from an autocomplete perspective this could be almost every time the user hits the space key.

insertion itself is ```O(L)``` time. but if the Trie is at capacity, the Trie must undergo an LFU prune, finding the LFU word can be done in is ```O(W)``` time (where W is the number of words in the Trie) and ```O(W)``` space. Deletion can be done in ```O(L)``` it, where ```L``` is the length of the word (just like normal insertion). Thus the LFU prune is ```O(L + W)``` time. if prune is called at almost every insertion becomes an``` O(L + W)``` operation. 

#### Do we have to take this performance hit? The answer is no.

A caching  algorithm proposed by Shah, Mitra, and Matani, can accomplish caching and finding the LFU word in ```O(1)``` time, this [Fast LFU Caching](http://dhruvbird.com/lfu.pdf) could bring the overall runtime of insertion back to ```O(L)``` time if implemented. If i had more time i would have implemented this caching scheme. 









