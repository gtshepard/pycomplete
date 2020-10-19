## Overview 

Thank for the opportunity to complete this project for the neeva 2021 Software Engineer New Grad Role. 

I chose to work on the text editor project as it best suits my interests and skill set. 

The project allowed for creative freedom. I chose to focus on adding additional features to the text editor and optimizing the features that I did add. 

I built an autocomplete library for the text editor called PyComplete. 

PyComplete suggests the  ```K``` most frequent words for a given prefix. PyComplete records  input words and adjusts their frequencies. When a prefix is given as input, the ```K``` most frequent words with that prefix are suggested. 

Suppose ```K = 3``` and one  records the words ``` what``` 10 times, ```when``` 4 times, and ```who``` 2 times. Then the prefix ```wh``` is given as input. PyComplete would suggest: ````what, when, who````. 

PyComplete by default remembers the 1000 most frequent words the user type. This is a parameter that the user can change. 

The PyComplete interface 

```python 
  # make pycomplete remember a word
  def record_word(words: str) -> Void:
  
  # the top k most frequent words with a given prefix
  def suggest_words(prefix: str, k: int) -> []:
```

## Understanding The Performance 

#### Suggest Words Operation 

The key operation for autocomplete is to be able to find all words with the same prefix. This operation must be efficient.

a naive to this problem can be implemented using a list and is done is ```O(N * M)``` time and O(N) space, where N is the number of words in the list, M is the length of the prefix. This is because we have to check M letters for the words in the list.


PyComplete uses a Trie (prefix tree) data structure to suggest words

a Trie reduces the complexity to ```O(P + J)```, where ```P``` is the number of words with the same prefix, and where J is the number of nodes needed to form ```P``` words
  
this is because once we reach the prefix in the Trie we have to construct all the words with the same prefix, and there could be as many as ```P``` of them and there may be as many as J nodes to visit to accumulate characters in order to form these``` P``` words. we reconstruct words in depth first manner starting from the end of the given prefix 

PyCompletes Trie is also space optimized. 

 Tries in general are M-ary trees. Where ```M``` is the number of children. Which have a space complexity ```O(M * N)``` where ```N```  is number of nodes 

A node in a Trie has a child pointer for every character that could be stored in the trie. thus if the number of characters is held constant, we reduce
the space complexity to ```O(N)``` where ```N``` is the number of nodes. PyCompletes Trie restricts the number of characters the Trie will store to 28. 26 of these characters for lowercase english alphabet plus two additional characters ```-``` and ```'``` characters to account for words like ```all-knowing``` and ```we're```. Thus our Trie has a space complexity O(N) where N is the number of nodes, because the width of Trie is constant (28 characters)

PyComplete not only suggests words based on prefix, but also based on the frequency that words are used. Thus when PyComplete makes a suggestion based on a prefix, it will be the K most frequent words with that prefix. 
Since this is a core operation of PyComplete and most likely takes place every time a user presses a key. Time Complexity Performance is favored over space compexity.   

we first find all ```P``` words with the same prefix ```O(P + J)``` time and then from there we find the K most frequent words. 
  
      - A naive approach would be to sort all P  words, and take the first ```K``` words. resulting ```O(K + P log P)```
      
      PyComplete uses a heap data structure to find the k most frequent words with the same prefix. PyComplete sacrifices to improve runtime. (naive approach uses O(1) space).the heap uses ```O(P)``` space and is created in ```O(P)``` time with heapify 
we then pop the ```K``` most frequent elements. Each pop is a constant time operation, but we do so ```K``` times. However every time an element is popped, a new max must be percolated to the top, since there are initially P elements in the heap,, percolate  takes O( log P) time, this results in a runtime of ```O(K log P)``` time for popping and element and percolating a  new element to the top. If we take into account building  the heap, we have ```O(P + (K log P))```, if ```K``` is small, which for autocomplete it should be, it is much closer to ```O(P + log P)``` which is quite an improvement over the naive solution. alittle space is sacrifice a little space for a reduction in runtime 

How does PyComplete store the frequency? the frequency of each word is stored at the last char (node) of each word in the Trie. Trie’s always have some value to denote the end of a word, thus no additional space is used. a frequency of 0 means that this node does not mark the end of the word.
     
   
 ### Record Words Operation 
 How does PyComplete collect the frequency for words? it uses the record_word() operation.  

The record_word operation  operates in ```O(L)``` time where ```L``` is the length of the word being recorded. a likely time this may be called is everytime a user finishes typing a word. 

The two operations behind record word are Trie search and Trie insertion both taking O(L) time. If the word is not in the Trie, it is inserted and its frequency is adjusted to 1. If the word already exists, its frequency is adjusted by 1. 
      
you may be wondering why PyComplete does not just store the frequency of the word in a map and update it when a word is found in the map. Why store the freqencey in the Trie? this would be ```O(1)``` access time to see if the word exists and to update the frequency. 

This is because PyComplete wants to keep suggest_words as efficient as possible regardless of its value of ```K```. if frequency was not stored in the trie getting, getting the frequency for the top K words, would take ```O(K)``` time. and if K is large this is a lot of overhead and will take a toll on PyComplete, because suggestions will be made almost every time a user presses a key. 
      
  
   
  
 ### Avoiding Mistakes and Slow Downs 
 
to keep suggest_words performance stable, PyComplete removes the least frequently used word after the Trie reaches it capacity (a parameter set by the user) this is for a few reasons, it keeps the space consumed by the Trie bay and words that the user rarely record disappear, but more importantly it reduces the number of words in the Trie, that is for any given prefix, it has the chance to reduce the number of of words P with the same Prefix. this keeps ```P``` from growing excessively large over (imagine if words were never deleted. because as ```P``` grows large, it hurts the runtime ```O(P + K log P)``` to construct all words with the same prefix. a core operation of PyComplete. 
 
 
Keeping suggest_words performance stable, comes with a cost. we sacrifice some performance in regards to the record_word operation. 

This is the cost of finding the Least Frequently Used (LFU) word and deleting it from the Trie when it reaches capacity. This means for a user, who is always at or around capacity, every time they record a word the Trie must be pruned.  this changes the cost of insertion which happens when the user records a word that is not in Trie. 

insertion itself is ```O(L)``` time. but if the Trie is at capacity, the Trie must undergo a LFU prune, finding the LFU word can be done in is ```O(W)``` time (where W is the number of words) and ```O(W)``` space. Deletion can be done in ```O(L)``` it, where ```L``` is the length of the word (just like normal insertion). thus insertion becomes an``` O(2L + W)``` operation. 

an algorithm proposed by Shah, Mitra, and Matani, can accomplish caching and finding the LFU word in ```O(1)``` time, this could bring the overall runtime of insertion back to ```O(L)``` time if implemented.


To avoid suggesting  misspelled  words, we only record words that appear in a dictionary (local dictionary file on Mac OS)  






