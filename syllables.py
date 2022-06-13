import nltk 

# You may need to run nltk.download('punkt')

def syllableCounter(word):

    original = word[0:]
    
    word = word.lower()
    
    # Found that syllables are essentially found by looking for the transition from a consonant to a vowel
    # This finds the number of syllables in a word by counting the number of times this occurs
    # If a word begins with a vowel, then the number of syllables starts at 1, since there might as well be an invisible consonant before the first vowel

    vowels = ["a", "e", "i", "o", "u", "y"] # Defines the vowels (including y for syllable purposes) 
    
    prevBool = word[0] in vowels # Whether the current (or previous) letter, first letter of the word, is a vowel or not

    # If the first letter is a vowel, then begin with 1 syllable
    if prevBool:
        tally = 1
    else: # If not, meaning it is a consonant, begin with 0
        tally = 0
        
    # While the word has at least one letter
    while len(word) > 0:
        
        #print(word)
        
        if word == "the":
            
            tally += 1
        
        # Is the next letter (the first letter in the current state of "word") vowel?
        currBool = word[0] in vowels

        # Prints out the word and whether the previous and current vowels are letters
        # print(word)
        # print("Previous vowel?: {}".format(prevBool))
        # print("Current Vowel: {}".format(currBool))

        if currBool != prevBool and currBool:
    
            if word != "e": # Makes sure the last letter "e" does not add an extra syllable
            
                tally += 1
            # print("increased")
            
        if word[1:] == "ed" and len(original) > 3:
        
            if word[0] not in ["d", "t"]:
                tally -= 1

        prevBool = currBool    

        word = word[1:]
        # print(tally)
        # print("--")
        
    return tally

def stringSyllables(string):
    words = [word for word in nltk.word_tokenize(string) if word.isalpha()]
    syls = [syllableCounter(word) for word in words]
    
    total = 0
    
    for syl in syls:
        total += syl
        
    avg = total/len(words)
    
    return words, syls, avg

testString = "Hey, my name is Jake, and I really like computers. Do you?"
wordList, sylList, avgSyls = stringSyllables(testString)

print("Words: {}".format(wordList))
print("Syllables: {}".format(sylList))
print("Avg. # Syllables: {}".format(avgSyls))
