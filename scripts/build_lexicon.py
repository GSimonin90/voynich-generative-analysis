from collections import Counter
import re

# --- CONFIGURATION ---
# Based on our previous analysis, we define the most common morphemes.
# We sort them by length (longest to shortest) to ensure correct matching.
COMMON_PREFIXES = ['ch', 'qo', 'sh', 'ok', 'da', 'o', 'c', 'q', 's', 'd']
COMMON_SUFFIXES = ['dy', 'in', 'ey', 'ol', 'ar', 'y', 'n', 'l', 'r', 'm']
MINIMUM_FREQUENCY = 15  # We ignore morphemes that appear fewer than 15 times to reduce noise.

def load_words(filename="voynich_super_clean.txt"):
    """Loads the corpus and returns a list of unique words."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        # Use 'set' to analyze only unique words, improving efficiency
        words = set(re.findall(r'[a-z]+', text.lower()))
        print(f"✅ Corpus '{filename}' loaded. Analyzing {len(words)} unique words.")
        return list(words)
    except FileNotFoundError:
        print(f"❌ ERROR: File '{filename}' not found.")
        return None

def peel_word(word):
    """
    "Peels" a word to extract its prefix, root, and suffix.
    Returns a tuple: (prefix, root, suffix).
    """
    original_word = word
    prefix_found = None
    suffix_found = None

    # 1. Look for the longest possible matching prefix
    for p in COMMON_PREFIXES:
        if word.startswith(p):
            prefix_found = p
            word = word[len(p):]  # Remove the prefix from the word
            break

    # 2. Look for the longest possible matching suffix from the remaining string
    for s in COMMON_SUFFIXES:
        if word.endswith(s):
            suffix_found = s
            word = word[:-len(s)]  # Remove the suffix
            break
    
    # 3. What remains is the root
    root = word

    # If the root is empty, the word consisted only of affixes (e.g., "dy").
    # In this case, we treat the original word as a root to avoid losing it.
    if not root:
        return None, original_word, None
        
    return prefix_found, root, suffix_found

def save_lexicon(counter, filename, header):
    """Saves a counter to a text file, sorted by frequency."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {header}\n")
        f.write("# Morpheme | Frequency\n")
        f.write("="*20 + "\n")
        # Filter out infrequent morphemes and sort the list
        for item, count in counter.most_common():
            if count >= MINIMUM_FREQUENCY:
                f.write(f"{item:<10} | {count}\n")
    print(f"✅ Lexicon saved to '{filename}'")

if __name__ == "__main__":
    words = load_words()
    if words:
        prefix_counter = Counter()
        root_counter = Counter()
        suffix_counter = Counter()

        # Analyze each unique word in the corpus
        for word in words:
            prefix, root, suffix = peel_word(word)
            
            if prefix:
                prefix_counter[prefix] += 1
            if root:
                root_counter[root] += 1
            if suffix:
                suffix_counter[suffix] += 1
        
        print("\n--- Morphological Analysis Complete ---")
        print(f"Found {len(prefix_counter)} unique prefixes.")
        print(f"Found {len(root_counter)} unique roots.")
        print(f"Found {len(suffix_counter)} unique suffixes.")

        # Save the results to our lexicon files
        save_lexicon(prefix_counter, "prefixes.txt", "Voynich Language Prefixes")
        save_lexicon(root_counter, "roots.txt", "Voynich Language Core Roots")
        save_lexicon(suffix_counter, "suffixes.txt", "Voynich Language Suffixes")