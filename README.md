# PyComplete an Autocomplete Library 

1. [Overview](#overview)
2. [How To Run This Project](#how-to-run-this-project)

### Overview 

PyComplete is an autocomplete library for python.

PyComplete suggests the  ```K``` most frequent words for a given prefix. PyComplete records  input words and adjusts their frequencies. When a prefix is given as input, the ```K``` most frequent words with that prefix are suggested. 

Suppose ```K = 3``` and one  records the words ``` what``` 10 times, ```when``` 4 times, ```who``` 2 times, and ```whale``` 1 time. Then the prefix ```wh``` is given as input. 

PyComplete would suggest: ````what, when, who````. 

PyComplete by default remembers the 1000 most frequent words the user type. This is a parameter that the user can change. 

### The PyComplete interface 

```python 
  # record word and update frequency 
  def record_word(words: str) -> Void:
  
  # the top k most frequent words with a given prefix
  def suggest_words(prefix: str, k: int) -> []:
```

## How To Run This Project

 - Make sure python3 and pip3 are installed 
 - navigate to project directory 
 - to install required dependencies type
 ``` pip3 install -r requirements.txt ```
 - for a quick demo run 
 ```python autocomplete.py```
 - To run test cases 
 ```pytest test_autocomplete.py ```
 - to use PyComplete in a project
 
```python
   import autocomplete as ac 
   import topktrie as tkt
```
 







