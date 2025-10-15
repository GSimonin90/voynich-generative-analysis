import re
from collections import Counter

# --- CONFIGURATION ---
BASELINE_FILE = "voynich_super_clean.txt"
TRANSCRIPTION_FILE = "voynich.txt"
ROOTS_FILE = "roots.txt"

CONTEXT_TO_TEST = {
    "name": "Pisces Folio Labels (f70r1)",
    "target_root": "kch",
    "folio_prefix": "f70r1" 
}

def load_lexicon(filename):
    """Loads the core roots lexicon, sorted by length (descending)."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            morphemes = [line.split('|')[0].strip() for line in f if not line.startswith('#') and '|' in line]
            morphemes.sort(key=len, reverse=True)
        return morphemes
    except (FileNotFoundError, IndexError):
        return None

def find_longest_root(word, roots):
    """Finds the single longest matching root from the lexicon within a word."""
    for root in roots:
        if root in word:
            return root
    return None

def calculate_final_lift(context_info):
    """Calculates the statistical lift using a precise, line-by-line context extraction method."""
    print(f"--- Final Statistical Lift for '{context_info['target_root']}' in '{context_info['name']}' ---")
    
    all_roots = load_lexicon(ROOTS_FILE)
    if not all_roots: return

    # 1. Create the BASELINE from the entire clean corpus
    try:
        with open(BASELINE_FILE, 'r', encoding='utf-8') as f:
            baseline_words = f.read().split()
        baseline_root_counts = Counter(find_longest_root(w, all_roots) for w in baseline_words)
    except FileNotFoundError:
        print(f"❌ ERROR: Baseline file '{BASELINE_FILE}' not found.")
        return

    # 2. Precisely extract CONTEXT words line by line from the original transcription
    try:
        with open(TRANSCRIPTION_FILE, 'r', encoding='utf-8') as f:
            transcription_lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ ERROR: Transcription file '{TRANSCRIPTION_FILE}' not found.")
        return
        
    context_words = []
    label_regex = re.compile(r'<' + re.escape(context_info['folio_prefix']) + r'\..*?>\s*(.*)')
    for line in transcription_lines:
        match = label_regex.search(line)
        if match:
            label_text = match.group(1)
            cleaned_text = re.sub(r'<!.*?>|[\?!,]', '', label_text).strip()
            context_words.extend(cleaned_text.split('.'))
    
    context_root_counts = Counter(find_longest_root(w, all_roots) for w in context_words if w)

    # 3. Calculate Frequencies
    target_root = context_info['target_root']
    observed_in_context = context_root_counts.get(target_root, 0)
    expected_in_baseline = baseline_root_counts.get(target_root, 0)

    if expected_in_baseline == 0 or not context_words:
        print("Cannot calculate lift: root not found in baseline or context is empty.")
        return

    observed_freq = observed_in_context / len(context_words)
    expected_freq = expected_in_baseline / len(baseline_words)

    # Prevent division by zero if observed_freq is 0
    if observed_freq == 0:
        lift_score = 0
    else:
        lift_score = observed_freq / expected_freq

    print("\n--- Quantitative Analysis Results ---")
    print(f"  Target Root:          '{target_root}'")
    print(f"  Total Words (Baseline): {len(baseline_words)}")
    print(f"  Total Words (Context):  {len(context_words)}")
    print("-" * 35)
    print(f"  Occurrences (Baseline): {expected_in_baseline}")
    print(f"  Occurrences (Context):  {observed_in_context}")
    print("-" * 35)
    print(f"  Expected Frequency:     {expected_freq:.6f} (or 1 in {int(1/expected_freq):,} words)")
    print(f"  Observed Frequency:     {observed_freq:.6f} (or 1 in {int(1/observed_freq) if observed_freq > 0 else 0:,} words)")
    print("-" * 35)
    print(f"  STATISTICAL LIFT SCORE: {lift_score:.2f}")

if __name__ == "__main__":
    calculate_final_lift(CONTEXT_TO_TEST)