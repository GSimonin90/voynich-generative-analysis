from collections import Counter
import re

def load_corpus(filename="voynich_super_clean.txt"):
    """Loads the corpus and returns a list of words."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        # Find all sequences of lowercase letters
        words = re.findall(r'[a-z]+', text.lower())
        print(f"✅ Corpus '{filename}' loaded successfully. Found {len(words)} words.")
        return words
    except FileNotFoundError:
        print(f"❌ ERROR: File '{filename}' not found. Make sure it's in the same directory.")
        return None

def analyze_affixes(words, position='start', length=1, top_n=5):
    """
    Analyzes the most common prefixes or suffixes and the stems they attach to.
    - position: 'start' for prefixes, 'end' for suffixes.
    - length: length of the affix to analyze (e.g., 1 or 2 characters).
    """
    if position == 'start':
        print(f"\n--- Analysis of {length}-character Prefixes ---")
        # Extract all prefixes of the specified length
        affixes = [word[:length] for word in words if len(word) > length]
    else:  # end
        print(f"\n--- Analysis of {length}-character Suffixes ---")
        # Extract all suffixes of the specified length
        affixes = [word[-length:] for word in words if len(word) > length]
    
    if not affixes:
        print("No affixes found with the specified parameters.")
        return

    affix_counts = Counter(affixes)
    print(f"🏆 Top {top_n} most common affixes:")
    for affix, count in affix_counts.most_common(top_n):
        print(f"  '{affix}' -> appears {count} times.")
        
        # Now, for each common affix, let's see which "stems" it attaches to
        if position == 'start':
            stems = [word[length:] for word in words if word.startswith(affix)]
        else:  # end
            stems = [word[:-length] for word in words if word.endswith(affix)]
        
        stem_counts = Counter(stems)
        print(f"    Attaches to {len(stem_counts)} different stems. The 3 most common are:")
        for stem, stem_count in stem_counts.most_common(3):
            print(f"      - '{stem}' ({stem_count} times)")

def analyze_ngrams(words, n=3, top_n=10):
    """
    Extracts and counts all character n-grams within words.
    This method is unbiased and looks for the fundamental 'building blocks'.
    """
    print(f"\n--- Analysis of {n}-grams (the {n}-letter 'building blocks') ---")
    all_ngrams = []
    for word in words:
        if len(word) >= n:
            # Create a list of all n-grams for the current word
            ngrams_in_word = [word[i:i+n] for i in range(len(word) - n + 1)]
            all_ngrams.extend(ngrams_in_word)
    
    if not all_ngrams:
        print("No n-grams found.")
        return

    ngram_counts = Counter(all_ngrams)
    print(f"🏆 Top {top_n} most common {n}-grams in the entire corpus:")
    for ngram, count in ngram_counts.most_common(top_n):
        print(f"  '{ngram}' -> appears {count} times.")

if __name__ == "__main__":
    voynich_words = load_corpus()
    if voynich_words:
        # 1. Analyze single-character prefixes and suffixes
        analyze_affixes(voynich_words, position='start', length=1, top_n=5)
        analyze_affixes(voynich_words, position='end', length=1, top_n=5)
        
        # 2. Analyze two-character prefixes and suffixes
        analyze_affixes(voynich_words, position='start', length=2, top_n=5)
        analyze_affixes(voynich_words, position='end', length=2, top_n=5)

        # 3. Unbiased analysis: find the most common 3-letter 'building blocks'
        analyze_ngrams(voynich_words, n=3, top_n=15)