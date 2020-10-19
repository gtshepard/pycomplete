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
import topktrie as topk 
from heapq import * 
class AutoComplete:

    def __init__(self):
        self.word_cache = WordCache()
        self.trie = topk.TopkTrie(file_path="one_hundred_most_common_words.txt")

    def __top_k_words__(self, key, k):
        # get last node of prefix in trie

        source = self.trie.get_end_of_prefix(key)
        words_with_same_prefix = []
        # build k words with specified prefix 
        if source:
            self.trie.construct_words(source, key, words_with_same_prefix)
        else:
            return []
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

        top_k_words = [(-x[0], x[1]) for x in top_k_words]
        return top_k_words

    def record_word(self, word):
        # to avoid suggesting misspelled words
        # we check it against our dicitonary
        # some words may not be recored that are infact words
        # becuase they are not in the dictionary
        # user has option to add words to dictionary 
        if word in self.word_cache.cache:
            have_seen = self.trie.search(word)
           # if have_seen:
                #print("search")
            if not have_seen:
                #print("insert")
                self.trie.insert(word)
    
    def suggest_words(self, prefix, k):
        suggested_words = self.__top_k_words__(prefix, k=k)
        suggested_words = [x[1] for x in suggested_words]
        return suggested_words

if __name__ == '__main__':

    a = AutoComplete()
    a.record_word("whale")
    a.record_word("whale")
    a.record_word("whale")
    print(a.trie.number_of_words)
    a.record_word("when")
    a.record_word("when")
    a.record_word("when")
    a.record_word("dog")
    a.record_word("dog")
    #a.trie.print_trie()
    #print(a.trie.number_of_words)
    #a.record_word("a")
    #a.record_word("a")
  #  a.record_word("a")
    a.suggest_words("wh", 5)
    



    


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

#  O(L + N*W) lookup O(L) time for prefix lookup. O(N*W) where N is the number of words that have the prefix abd W is
# the is the lenght of the longest word  
# 
# O(W * L * N) where L is the max word length (depth) and N is the number of words and W is the width of the tree
# however W is constant at 26, thus we have O(L * N) space
# compared to a series of maps its more efficient memory wise if we you had as hash map for each word
# 

