


class WordCache:

    def __init__(self):
        self.cache = set()
        self.build_cache()

    def build_cache(self):
        file_paths = ["/usr/share/dict/words", "one_hundred_most_common_words.txt"]
        n = len(file_paths)
        for i in range(n):
            with open(file_paths[i]) as input_dictionary:
                for line in input_dictionary:
                    words = line.strip().split(" ")
                    for word in words:
                        if word.isalpha():                
                            self.cache.add(word)

    def is_valid_word(self, s):
        return True if s in self.cache else False 
      
class Node:
    def __init__(self, char=''):
        self.children = [None] * 26
        # marks frequency at end
        self.end_of_word = 0
        self.char = char 

    def mark_as_leaf(self):
        self.end_of_word += 1 
    
    def unmark_as_leaf(self):
        self.end_of_word -= 1
from heapq import *

class LfuTrie:

    def __init__(self):
        self.word_freq = {}
        self.word_freq_inv = {}
        self.root = Node()
        self.build_trie("one_hundred_most_common_words.txt")
    #ascii a char value is 141,
    # b is 142 
    # b - a = 1
    # if we index from 0 to 25 
    # b is in position 1 
    # thus in a trie node its stored
    # in children[1]
    def get_index(self, t):
        return ord(t) - ord('a')
    
    def insert(self, key):
        if not key:
            return 

        key = key.lower()
        curr_node = self.root
        self.word_freq[key] = self.word_freq.get(key, 0) + 1
        # maybe make text area only take up 3/4 of page
        for level in range(len(key)):
            # get the index for the levelth char 
            # of the word to insert
            index = self.get_index(key[level])
            # if char does not exist
            if not curr_node.children[index]:
                # insert char at current level 
                curr_node.children[index] = Node(key[level])

            curr_node = curr_node.children[index]

        # mark as word end by incrementing frequncy
        curr_node.mark_as_leaf()
   

    def search(self, key):
        if not key:
            return False
        
        key = key.lower()
        curr_node = self.root
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]
        
        if curr_node and curr_node.end_of_word > 0:
            self.word_freq[key] += 1
            curr_node.mark_as_leaf()
            return True 
        else:
            return False

    def build_trie(self, file_path):
        with open(file_path) as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split('\n')
                for word in words:
                    self.insert(word)

    def print_trie(self):
        result = []
        self.dfs(self.root, '', result)
        print(result)

    # trie is a trie where each node has 26 chidren 
    # thus we can use DFS to travese it and rebuild words
    def construct_k_words(self, node, word, res, k=3):
        
        if node.end_of_word > 0:
            res.append((node.end_of_word, word))

        for child in node.children:
            if child:
                self.construct_k_words(child, word + child.char, res, k)
    
    def get_end_of_prefix(self, prefix):
        key = prefix.lower()
        curr_node = self.root
        # find end of prefix in trie 
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]

        return curr_node
    
    def delete_least_freq(self):
        #self.least_freq_used
        pass

    def least_freq_used(self):
        least_freq = (float('inf'), None)
        for word, f in self.word_freq.items():
            if f < least_freq[0]:
                least_freq = (f, word)

        return least_freq
class AutoComplete:

    def __init__(self):
        self.word_cache = WordCache()
        self.trie = LfuTrie()

    def __top_k_words__(self, key, k):
        # get last node of prefix in trie
        source = self.trie.get_end_of_prefix(key)
        words_with_same_prefix = []
        # build k words with specified prefix 
        self.trie.construct_k_words(source, key, words_with_same_prefix, k=k)

        # same_prefix.sort(reverse=True) # could be rather large 
        # maybe build heap ? this would be quicker O(N) to build heap
        # O(N + K)better than N Log N, K is cconstant for us 
        # k pops to get the element 
        # 
        # heapify(same_prefix)
        n = len(words_with_same_prefix)
        # negate frequncy for max heap
        words_with_same_prefix = [(-x[0], x[1]) for x in words_with_same_prefix]
        # create heap in O(N) time 
        heapify(words_with_same_prefix)
        top_k_words = []

        # pop k elements
        for i in range(k):
            if words_with_same_prefix:
                top_k_words.append(heappop(words_with_same_prefix))

        return top_k_words

    def record_word(self, word):
        if word in self.word_cache.cache:
            # have to adjust insert so size does not execeede 100
            have_seen = self.trie.search(word)
            if not have_seen:
                self.trie.insert(word)
    
    def suggest_words(self, prefix, top_k):
        suggested_words = self.__top_k_words__(prefix,k=top_k)
        suggested_words = [x[1] for x in suggested_words]
        self.trie.least_freq_used()
        return suggested_words

if __name__ == '__main__':

    a = AutoComplete()
    a.record_word("whale")
    a.record_word("whale")
    a.record_word("whale")
    a.record_word("when")
    a.record_word("when")
    a.record_word("when")
    print(a.suggest_words("wh", 5))


    # file_path = "one_hundred_most_common_words.txt"
    #t.build_trie(file_path)
    #t.build_k_words_with_same_prefix("wh",k=5)

    # how to add frequency to trie?
    # 1+ represents word end 
    # 0 represents no word
    # if try inserted, its mark is set to 1
    # if a word is searched for and found frequency value is + 1 
    
    # if we type a word and hit space, that is not in the trie, then the word 
    # is pushed into the trie
    # the issue here is users may type things that are not words
    # to eliminate this problem we will check the words against the word dictionary
    # and the 100 most common words dictionary to make sure to only insert real words
    # we sacrfice a bit of space, for effiecney and accuracy.
    # we keep the trie smaller by not adding uneeded content and accruate 
    # if we restict the size of the trie to 100, we will never run into search issues 
    # and it effectilvely operates in constant time 

    # 1. prevent strings that are not real words being placed in trie 
    # this happens when user hits space when a word is misspelled.
    # we check the users input against a 2 word banks - 100 most common words
    # and the dictionary 

    # 2. suggested word should be sorted by frequency 
    # this can done by putting frquncy in a tuple with the word 
    # then sorting by the frequency of the the first value in the tuple


    #2. to keep trie to size 100, we must delete LRU 
    # this means that we want to delete the word with the smallest freqency first 
    # 

'''
    with open("/usr/share/dict/words") as input_dictionary:
        for line in input_dictionary:
            words = line.strip().split(" ")
            for word in words:
                if word.isalpha():                
                    # all_words.append(word)
                    t.insert(word)
  '''
#  O(L + N*W) lookup O(L) time for prefix lookup. O(N*W) where N is the number of words that have the prefix abd W is
# the is the lenght of the longest word  
# 
# O(W * L * N) where L is the max word length (depth) and N is the number of words and W is the width of the tree
# however W is constant at 26, thus we have O(L * N) space
# compared to a series of maps its more efficient memory wise if we you had as hash map for each word
# 

