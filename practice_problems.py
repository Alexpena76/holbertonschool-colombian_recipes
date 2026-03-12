#1 My answer:

def repeating():
    """Returns the first character which isn't repeating in a string, or None if there is no such character-"""
    s = "String"
    for a in s:
        if s.count(a) == 1:
            return a
    return None

#1 The answer:

def first_non_repeating(word):
    # Step 1: count every character in one pass
    counts = {}
    for char in word:
        counts[char] = counts.get(char, 0) + 1
    
    # Step 2: find the first one with count of 1
    for char in s:
        if counts[char] == 1:
            return char
    
    return "_"

#2 My answer (correct):
def is_anagram(s, t):
    """Returns true if the two strings are anagrams of each other, and false otherwise."""
    count_of_s = {}
    count_of_t = {}
    for char in s:
        count_of_s[char] = count_of_s.get(char, 0) + 1
    for char in t:
        count_of_t[char] = count_of_t.get(char, 0) + 1
    return count_of_s == count_of_t

#3 My answer:
def target_sum(nums, target):
    """Returns the indices of the two numbers that add up to the target, or None if there is no such pair."""
    for i, val in enumerate(nums):
        if target - val == j