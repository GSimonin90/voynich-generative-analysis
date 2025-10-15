from collections import Counter
import re

# --- CONFIGURATION ---
# These lists must be consistent with the ones used in build_lexicon.py
COMMON_PREFIXES = ['ch', 'qo', 'sh', 'ok', 'da', 'o', 'c', 'q', 's', 'd']
COMMON_SUFFIXES = ['dy', 'in', 'ey', 'ol', 'ar', 'y', 'n', 'l', 'r', 'm']
MINIMUM_RULE_FREQUENCY = 5 # A combination must appear at least 5 times to be considered a "rule".

def load_lexicon(filename):
    """Loads a lexicon file (prefixes, roots, or suffixes) into a set for fast lookups."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Read lines, strip whitespace, and ignore comments or empty lines
            morphemes = {line.split('|')[0].strip() for line in f if not line.startswith('#') and '|' in line}
        print(f"✅ Lexicon '{filename}' loaded successfully with {len(morphemes)} morphemes.")
        return morphemes
    except FileNotFoundError:
        print(f"❌ ERROR: Lexicon file '{filename}' not found. Please run build_lexicon.py first.")
        return None

def load_words(filename="voynich_super_clean.txt"):
    """Loads the corpus and returns a list of all words (not unique)."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        words = re.findall(r'[a-z]+', text.lower())
        print(f"✅ Corpus '{filename}' loaded with {len(words)} total words.")
        return words
    except FileNotFoundError:
        print(f"❌ ERROR: Corpus file '{filename}' not found.")
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
            word = word[len(p):]
            break

    # 2. Look for the longest possible matching suffix from the remaining string
    for s in COMMON_SUFFIXES:
        if word.endswith(s):
            suffix_found = s
            word = word[:-len(s)]
            break
    
    # 3. What remains is the root
    root = word

    if not root:
        return None, original_word, None
        
    return prefix_found, root, suffix_found

def save_rules(counter, filename, header):
    """Saves the discovered combination rules to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {header}\n")
        f.write("# Combination      | Frequency\n")
        f.write("="*28 + "\n")
        for item, count in counter.most_common():
            if count >= MINIMUM_RULE_FREQUENCY:
                combination_str = f"{item[0]}-{item[1]}"
                f.write(f"{combination_str:<18} | {count}\n")
    print(f"✅ Grammar rules saved to '{filename}'")

if __name__ == "__main__":
    # Load the morpheme dictionaries we created in Phase 1
    valid_prefixes = load_lexicon("prefixes.txt")
    valid_roots = load_lexicon("roots.txt")
    valid_suffixes = load_lexicon("suffixes.txt")
    
    # Load the full corpus to analyze all word occurrences
    words = load_words()

    if all([valid_prefixes, valid_roots, valid_suffixes, words]):
        prefix_root_counter = Counter()
        root_suffix_counter = Counter()

        # Analyze every word in the corpus
        for word in words:
            prefix, root, suffix = peel_word(word)

            # We only record a rule if all parts are valid members of our lexicons
            is_prefix_valid = prefix in valid_prefixes
            is_root_valid = root in valid_roots
            is_suffix_valid = suffix in valid_suffixes

            if is_prefix_valid and is_root_valid:
                prefix_root_counter[(prefix, root)] += 1
            
            if is_root_valid and is_suffix_valid:
                root_suffix_counter[(root, suffix)] += 1
        
        print("\n--- Grammar Rule Analysis Complete ---")
        print(f"Found {len(prefix_root_counter)} unique prefix-root combinations.")
        print(f"Found {len(root_suffix_counter)} unique root-suffix combinations.")

        # Save the discovered rules to files
        save_rules(prefix_root_counter, "prefix_root_rules.txt", "Prefix-Root Combination Rules")
        save_rules(root_suffix_counter, "root_suffix_rules.txt", "Root-Suffix Combination Rules")