import pytest as py
import topktrie as topk
import autocomplete as ac 
# test trie 
class TestTopK:

    def test_get_index(self):
        trie = topk.TopkTrie(file_path=None)
        # characters are always converted lower case
        index1 = trie.get_index('y')
        index2 = trie.get_index('b')
        index3 = trie.get_index('e')
        
        assert index1 == 24 and index2 == 1 and index3 == 4

    def test_insert_basic(self):
        trie = topk.TopkTrie(file_path=None)
        trie.insert('neeva')
        
        #insert neeva
        n_index = trie.get_index('n')
        e_index = trie.get_index('e')
        v_index = trie.get_index('v')
        a_index = trie.get_index('a')

        has_n = None 
        has_e_1 = None 
        has_e_2 = None 
        has_v = None 
        has_a = None 
        end_of_word = 0
        # check if trie contains proper structure after word insertion
        has_n = trie.root.children[n_index]
        if has_n:
            has_e_1 = has_n.children[e_index]

        if has_e_1:
            has_e_2 = has_e_1.children[e_index]

        if has_e_2:
            has_v = has_e_2.children[v_index]

        if has_v:
            has_a = has_v.children[a_index]

        if has_a:
            if has_a.end_of_word > 0:
                end_of_word = True 

        assert (has_n and has_n and has_e_1 and has_e_2 and has_v and has_a and end_of_word)

    def test_insert_multiple_words(self):
        words = ['apple','cookie', 'carrot', 'cracker','camera', 'needle' , 'neeva']
        trie = topk.TopkTrie(file_path=None)
    
        for w in words:
            trie.insert(w)

        word_cache = {}
        for w in words:
            word_cache[w] = w

        constructed_words = []
        trie.construct_words(trie.root, '', constructed_words)
       
        #filter out frequencies
        constructed_words = [x[1] for x in constructed_words]
        seen_all_words = True
        
        for w in constructed_words:
            if w not in word_cache:
                seen_all_words = False 
                break

        assert seen_all_words
        
    def test_insert_many_words(self):
        # add many words to set 
        file_paths = ["one_hundred_most_common_words.txt"]
        set_of_words = set()

        n = len(file_paths)
        for i in range(n):
            with open(file_paths[i]) as input_dictionary:
                for line in input_dictionary:
                    words = line.strip().split('\n')
                    for word in words:
                        set_of_words.add(word.lower())

      
        trie = topk.TopkTrie(file_path=None)
        trie.build_trie(file_paths[0])
        constructed_words = []
        trie.construct_words(trie.root, '', constructed_words)
        
        #filter out frequencies
        constructed_words = [x[1] for x in constructed_words]

        seen_all_words = True  
      
        seen_all_words = True 
        for w in constructed_words:
           if w not in set_of_words: 
                seen_all_words = False
                break 
       
        assert seen_all_words

    def test_search_basic(self):
        trie = topk.TopkTrie(file_path="one_hundred_most_common_words.txt")
        found = trie.search("I")
        assert found

    def test_search_many(self):
        file_path = "one_hundred_most_common_words.txt"
        trie = topk.TopkTrie(file_path=file_path)
        errors = []

        with open(file_path) as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split('\n')
                for word in words:
                    if not trie.search(word):
                        errors.append("error (test_search_many) %s not found in trie"%word)

        assert not errors

    def test_delete_basic(self):
        file_path = "one_hundred_most_common_words.txt"
        trie = topk.TopkTrie(file_path=file_path)

        trie.delete("when")

        #construct and clean words
        constructed_words = []
        trie.construct_words(trie.root, '', constructed_words)  
        constructed_words = [x[1] for x in constructed_words]
        set_of_words_in_trie = set(constructed_words)
        
        assert not "when" in set_of_words_in_trie

    def test_delete_many(self):

        words_to_delete = ["how", "man","in", "into", "a","her","here","if","make","look","like", "him","I", "his"]
        trie = topk.TopkTrie(file_path="one_hundred_most_common_words.txt")

        # detele words in list
        for w in words_to_delete:
            trie.delete(w)
        
        #construct and clean words from trie
        constructed_words = []
        trie.construct_words(trie.root, '', constructed_words)  
        constructed_words = [x[1] for x in constructed_words]
        set_of_words_in_trie = set(constructed_words)

        # check if words were deleted
        is_deleted = True 
        for w in words_to_delete:
            if w in set_of_words_in_trie:
                is_deleted = False
                break

        assert is_deleted

    def test_get_lfu(self):
        trie = topk.TopkTrie()
     

        animals = ['monkey', 'bird', 'dog', 'cat', 'zebra']
        for a in animals:
            trie.insert(a)
        n = 4
        i = 0
        while i < n:
            for a in animals:
                if a != "bird":
                    trie.search(a)
            i += 1

        trie.search("bird")
        #find least frequently used word (used meaning searched) 
        lfu_word = trie.get_lfu()
        assert "bird" == lfu_word

    def test_lfu_prune(self):
        trie = topk.TopkTrie()
        animals = ['monkey', 'bird', 'dog', 'cat', 'zebra']
        for a in animals:
            trie.insert(a)
        n = 4
        i = 0
        # make bird the least frequently used word 
        while i < n:
            for a in animals:
                if a != "bird":
                    trie.search(a)
            i += 1
        trie.search("bird")

        trie.lfu_prune()
        constructed_words = []
        trie.construct_words(trie.root, '', constructed_words)  
        constructed_words = [x[1] for x in constructed_words]
        set_of_words_in_trie = set(constructed_words)
        
        is_deleted_freq = "bird" not in trie.word_freq
        is_deleted = "bird" not in set_of_words_in_trie

        assert is_deleted and is_deleted_freq

    def test_get_end_of_prefix(self):
        trie = topk.TopkTrie(file_path="one_hundred_most_common_words.txt")
        node = trie.get_end_of_prefix("whe")
        assert node.char == "e"

class TestAutoComplete:

    def test_record_word(self):

        autocomplete = ac.AutoComplete()
        autocomplete.record_word("animal")
        autocomplete.record_word("animal")
        autocomplete.record_word("animal")

        # animal should inserted into trie with frequency of 3 
        constructed_words = []
        autocomplete.trie.construct_words(autocomplete.trie.root, '', constructed_words)  
        word_set = set(constructed_words)
    
        assert (3, 'animal') in word_set


    def test_record_word_many(self):
        autocomplete = ac.AutoComplete()
        record = [(50, "animal"), (100, "dog"), (65, "bird")]
       
        i = 0
        for f, w in record:
            while i < f:
                autocomplete.record_word(w)
                i += 1
            i = 0

        constructed_words = []
        autocomplete.trie.construct_words(autocomplete.trie.root, '', constructed_words)  
        word_set = set(constructed_words)
        
        print(word_set)

        is_recorded = True 
        for pair in record:
            if pair not in word_set:
                is_recorded = False 
                break

        assert is_recorded

    def test_top_k_words(self):
        # given a value k, and prefix, we should get the k most frequent words with given prefix 
        autocomplete = ac.AutoComplete()
        # (frequency, word)
        record = [(50, "when"), (100, "what"), (65, "which"), (67, "bird"), (102, "we")]
       
        # record word each word f number of times
        # where f is the frequency of the word 
        # found in recrod array aboive
        i = 0
        for f, w in record:
            while i < f:
                autocomplete.record_word(w)
                i += 1
            i = 0

        top_k = autocomplete.__top_k_words__("wh", k=3)
        expected = [(101, "what"), (66, "which"), (51, "when")]

        n, m = len(expected), len(top_k)
        is_top_k = True if n == m else False

        # both lists match
        for i in range(n):
            tk_f, tk_w = top_k[i]
            ex_f, ex_w = expected[i]
            if ex_f != tk_f or ex_w != tk_w:
                is_top_k = False 
                break 

        assert is_top_k

    def test_suggest_words(self):
        
        autocomplete = ac.AutoComplete()
        #(frequency, word)
        record = [(50, "when"), (100, "what"), (65, "which"), (67, "bird"), (102, "we")]
       
        i = 0
        for f, w in record:
            while i < f:
                autocomplete.record_word(w)
                i += 1
            i = 0

        top_k = autocomplete.suggest_words("wh", k=3)
        expected = ["what", "which", "when"]
        assert top_k == expected


    