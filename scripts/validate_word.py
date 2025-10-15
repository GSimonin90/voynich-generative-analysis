import re

# --- CONFIGURATION ---
# These lists must be consistent with the ones used in our previous scripts.
COMMON_PREFIXES = ['ch', 'qo', 'sh', 'ok', 'da', 'o', 'c', 'q', 's', 'd']
COMMON_SUFFIXES = ['dy', 'in', 'ey', 'ol', 'ar', 'y', 'n', 'l', 'r', 'm']

def load_lexicon(filename):
    """Loads a lexicon file (e.g., roots.txt) into a set for fast lookups."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            morphemes = {line.split('|')[0].strip() for line in f if not line.startswith('#') and '|' in line}
        print(f"✅ Lexicon '{filename}' loaded with {len(morphemes)} morphemes.")
        return morphemes
    except FileNotFoundError:
        print(f"❌ ERROR: Lexicon file '{filename}' not found. Please run the previous scripts first.")
        return None

def load_rules(filename):
    """Loads a rule file (e.g., prefix_root_rules.txt) into a set of tuples."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            rules = set()
            for line in f:
                if not line.startswith('#') and '|' in line:
                    combination = line.split('|')[0].strip()
                    parts = tuple(combination.split('-'))
                    if len(parts) == 2:
                        rules.add(parts)
        print(f"✅ Ruleset '{filename}' loaded with {len(rules)} rules.")
        return rules
    except FileNotFoundError:
        print(f"❌ ERROR: Rule file '{filename}' not found. Please run find_grammar_rules.py first.")
        return None

def peel_word(word):
    """
    "Peels" a word to extract its prefix, root, and suffix.
    Returns a tuple: (prefix, root, suffix).
    """
    original_word = word
    prefix_found = None
    suffix_found = None

    for p in COMMON_PREFIXES:
        if word.startswith(p):
            prefix_found = p
            word = word[len(p):]
            break

    for s in COMMON_SUFFIXES:
        if word.endswith(s):
            suffix_found = s
            word = word[:-len(s)]
            break
    
    root = word

    if not root:
        return prefix_found, "", suffix_found # Return empty string for root if none
        
    return prefix_found, root, suffix_found

class VoynichValidator:
    """A class to validate if a word conforms to the discovered Voynich grammar."""
    def __init__(self):
        print("--- Initializing Voynich Grammatical Validator ---")
        self.prefixes = load_lexicon("prefixes.txt")
        self.roots = load_lexicon("roots.txt")
        self.suffixes = load_lexicon("suffixes.txt")
        self.prefix_root_rules = load_rules("prefix_root_rules.txt")
        self.root_suffix_rules = load_rules("root_suffix_rules.txt")
        
        self.is_ready = all([self.prefixes, self.roots, self.suffixes, 
                             self.prefix_root_rules, self.root_suffix_rules])
        if self.is_ready:
            print("✅ Validator is ready.")
        else:
            print("❌ Validator initialization failed due to missing files.")

    def is_valid_word(self, word):
        """
        Checks if a word is 'grammatically legal' according to our model.
        Returns True if valid, False otherwise.
        """
        if not self.is_ready:
            print("Validator is not ready. Cannot perform check.")
            return False

        # RULE 1: Check if the entire word is a known root.
        if word in self.roots:
            print(f"'{word}' -> ✅ ACCEPTED: Word is a known core root.")
            return True

        prefix, root, suffix = peel_word(word)

        # RULE 2: Check for Prefix + Suffix structure (no root).
        if prefix and suffix and not root:
            # For now, let's accept any valid prefix + suffix combination.
            # A more advanced model could have specific prefix-suffix rules.
            if prefix in self.prefixes and suffix in self.suffixes:
                 print(f"'{word}' -> ✅ ACCEPTED: Valid Prefix-Suffix structure ('{prefix}-{suffix}').")
                 return True

        # RULE 3: Check for Prefix + Root + Suffix structure.
        if root not in self.roots:
            print(f"'{word}' -> ❌ REJECTED: Root '{root}' not found in lexicon.")
            return False
        if prefix and prefix not in self.prefixes:
            print(f"'{word}' -> ❌ REJECTED: Prefix '{prefix}' not found in lexicon.")
            return False
        if suffix and suffix not in self.suffixes:
            print(f"'{word}' -> ❌ REJECTED: Suffix '{suffix}' not found in lexicon.")
            return False

        if prefix and (prefix, root) not in self.prefix_root_rules:
            print(f"'{word}' -> ❌ REJECTED: Combination rule '{prefix}-{root}' not found.")
            return False
        if suffix and (root, suffix) not in self.root_suffix_rules:
            print(f"'{word}' -> ❌ REJECTED: Combination rule '{root}-{suffix}' not found.")
            return False
            
        print(f"'{word}' -> ✅ ACCEPTED: Follows all discovered grammatical rules.")
        return True


if __name__ == "__main__":
    validator = VoynichValidator()
    
    if validator.is_ready:
        print("\n--- Testing some words ---")
        validator.is_valid_word("chedy")
        validator.is_valid_word("qokeedy")
        validator.is_valid_word("daiin")
        validator.is_valid_word("shey")

        print("\n--- Testing some 'illegal' or invented words ---")
        validator.is_valid_word("galaxy") 
        validator.is_valid_word("cheyqo") 
        validator.is_valid_word("qokain")