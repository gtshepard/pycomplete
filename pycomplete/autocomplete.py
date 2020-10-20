class WordCache:

    def __init__(self):
        self.cache = set()
        self.build_cache()

    def build_cache(self):
        file_paths = ["/usr/share/dict/words", "one_hundred_most_common_words.txt", ]
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
        self.trie = topk.TopkTrie(file_path="one_thousand_words.txt")

    def __top_k_words__(self, key, k):
        # get last node of prefix in trie

        source = self.trie.get_end_of_prefix(key)
        words_with_same_prefix = []
        # build k words with specified prefix 
        if source:
            self.trie.construct_words(source, key, words_with_same_prefix)
        else:
            return []
        
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
        # avoid recording mispelled words
        # only words in macOS dictionary checked
        if word in self.word_cache.cache:
            have_seen = self.trie.search(word)
            if not have_seen:
                self.trie.insert(word)
    
    def suggest_words(self, prefix, k):
        suggested_words = self.__top_k_words__(prefix, k=k)
        suggested_words = [x[1] for x in suggested_words]
        return suggested_words

if __name__ == '__main__':

    autocomplete = AutoComplete()
    print("---------------------------------------------")
    print("            Welcome to PyComplete!           ")
    print("---------------------------------------------")
    print("PyComplete is preloaded with 1000 words.")
    print("Each word has a frequency of 1.")
    print("This demo changes the frequeny of some words.") 
    print("Then its prompt PyComplete for a suggestion!")
    print("-----------------------------------------------")

    n, m, p, q = 100, 40, 20, 10 
    for i in range(n):
        autocomplete.record_word("what")
    
    print("what has been recorded %i times"%n)

    for i in range(m):
        autocomplete.record_word("when")

    print("what has been recorded %i times"%m)
   
    for i in range(p):
         autocomplete.record_word("who")
    
    print("what has been recorded %i times"%p)

    for i in range(q):
        autocomplete.record_word("who")
    
    print("what has been recorded %i times"%q)
    print("""Suggest 3 most frequent words with prefix 'wh'""")
    print(autocomplete.suggest_words("wh", k=3))

    print("-----------------------------------------------")
    for i in range(n):
        autocomplete.record_word("cook")
    print("Cook has been recorded %i times"%n)

    for i in range(m):
        autocomplete.record_word("coat")
    print("Cook has been recorded %i times"%m)

    print("""Suggest 5 most frequent words with prefix 'co'""")
    print(autocomplete.suggest_words("co", k=5))

    print("-----------------------------------------------")
    print("be sure to checkout the testcases test_autocomplete.py")
    print("""run them with 'pytest test_autocomplete.py'""")
    print("-----------------------------------------------")
    print("Thanks for Watching The PyComplete Demo =[0.0]  ...!")
    print("-----------------------------------------------")
    print(" =[0.0] see you soon =[0.0] ...!")
    print("-----------------------------------------------")
