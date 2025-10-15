import re
from collections import defaultdict

# --- CONFIGURATION ---
# The roots we want to hunt for in this run.
# Let's start by looking for candidates for Venus and Jupiter.
# From the frequency table, 'ke' peaks in Taurus (f71r), a Venus sign.
# 'da' and 'aii' are frequent in Pisces (f70r1), a Jupiter sign.
ROOTS_TO_TRACK = ['che']

TRANSCRIPTION_FILE = "voynich.txt"
ROOTS_FILE = "roots.txt"
ZODIAC_FOLIOS_TO_ANALYZE = [
    'f70r1', 'f70r2', 'f70v1', 'f70v2', # Pisces & Aries
    'f71r', 'f71v',                   # Taurus & Gemini
    'f72r1', 'f72r2', 'f72r3',         # Cancer
    'f72v1', 'f72v2', 'f72v3',         # Leo
    'f73r', 'f73v'                    # Virgo & Libra
]

def load_lexicon(filename):
    """Loads the core roots lexicon, sorted by length (descending)."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            morphemes = [line.split('|')[0].strip() for line in f if not line.startswith('#') and '|' in line]
            morphemes.sort(key=len, reverse=True)
        print(f"✅ Lexicon '{filename}' loaded with {len(morphemes)} core roots.")
        return morphemes
    except FileNotFoundError:
        print(f"❌ ERROR: Lexicon file '{filename}' not found.")
        return None

def find_longest_root(word, roots):
    """Finds the single longest matching root from the lexicon within a word."""
    for root in roots:
        if root in word:
            return root
    return None

def track_patterns_by_longest_root(roots_to_track, all_roots, folios, filename):
    """
    Tracks occurrences of specific roots by identifying the longest root in each word
    and reporting the label numbers where the target roots are found.
    """
    print(f"--- Tracking Patterns for Roots {roots_to_track} Across Zodiac Folios ---")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        print(f"✅ Transcription file '{filename}' loaded successfully.")
    except FileNotFoundError:
        print(f"❌ ERROR: Original transcription file '{filename}' not found.")
        return

    # Use defaultdict to easily append to lists
    pattern_map = defaultdict(lambda: defaultdict(list))

    for folio_prefix in folios:
        label_regex = re.compile(r'<' + re.escape(folio_prefix) + r'\.(\d+),@\w+;\w+>\s*(.*)')
        
        for line in all_lines:
            match = label_regex.search(line)
            if match:
                label_number = int(match.group(1))
                label_text = match.group(2)
                
                cleaned_text = re.sub(r'<!.*?>|[\?!,]', '', label_text).strip()
                words_in_label = cleaned_text.split('.')

                for word in words_in_label:
                    longest_root = find_longest_root(word, all_roots)
                    if longest_root and longest_root in roots_to_track:
                        pattern_map[folio_prefix][longest_root].append(label_number)

    # --- Print the final report ---
    print("\n--- Pattern Analysis Results (Longest Root Method) ---")
    for folio, root_data in pattern_map.items():
        print(f"\n  ## Folio {folio.upper()}:")
        if not root_data:
            print("    No target roots found.")
            continue
        for root, labels in root_data.items():
            sorted_labels = sorted(list(set(labels)))
            print(f"    Root '{root}': Found in Labels -> {sorted_labels}")


if __name__ == "__main__":
    all_roots_lexicon = load_lexicon(ROOTS_FILE)
    if all_roots_lexicon:
        track_patterns_by_longest_root(ROOTS_TO_TRACK, all_roots_lexicon, ZODIAC_FOLIOS_TO_ANALYZE, TRANSCRIPTION_FILE)