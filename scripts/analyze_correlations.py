import re
import os
from collections import Counter

def load_lexicon(filename="roots.txt"):
    """Loads the core roots lexicon into a set for fast lookups."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            morphemes = {line.split('|')[0].strip() for line in f if not line.startswith('#') and '|' in line}
        print(f"✅ Lexicon '{filename}' loaded with {len(morphemes)} core roots.")
        return morphemes
    except FileNotFoundError:
        print(f"❌ ERROR: Lexicon file '{filename}' not found. Please run build_lexicon.py first.")
        return None

def load_words_from_section(filepath):
    """Loads all words from a given section file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        return re.findall(r'[a-z]+', text.lower())
    except FileNotFoundError:
        print(f"⚠️ Warning: Section file '{filepath}' not found.")
        return []

def analyze_correlations(sections_dir="sections"):
    """
    Analyzes the frequency of core roots across different manuscript sections
    to find statistically significant keywords for each topic.
    """
    print("--- Starting Correlation Analysis: Roots vs. Thematic Sections ---")
    
    core_roots = load_lexicon()
    if not core_roots:
        return

    section_files = [f for f in os.listdir(sections_dir) if f.endswith('.txt')]
    if not section_files:
        print(f"❌ ERROR: No section files found in the '{sections_dir}' directory.")
        return
        
    # Step 1: Load all words and count frequencies for each section
    section_data = {}
    for filename in section_files:
        section_name = filename.replace('.txt', '')
        filepath = os.path.join(sections_dir, filename)
        words = load_words_from_section(filepath)
        section_data[section_name] = {
            "words": words,
            "word_count": len(words),
            "freq_dist": Counter(words)
        }

    # Step 2: For each root, calculate its relevance score for each section
    results = {section_name: {} for section_name in section_data}
    
    for root in core_roots:
        # Calculate the total occurrences of the root across the entire manuscript
        total_root_occurrences = sum(section['freq_dist'][root] for section in section_data.values())
        total_words_in_manuscript = sum(section['word_count'] for section in section_data.values())
        
        if total_root_occurrences == 0:
            continue
            
        # Calculate the root's average frequency across the whole manuscript (baseline)
        baseline_freq = total_root_occurrences / total_words_in_manuscript
        
        for section_name, data in section_data.items():
            if data['word_count'] == 0:
                continue
                
            # Calculate the root's frequency within this specific section
            section_freq = data['freq_dist'][root] / data['word_count']
            
            # Calculate the relevance score (a simple TF-IDF-like logic)
            # A score > 1 means the root is more frequent in this section than average.
            # A score >> 1 indicates a strong correlation.
            if baseline_freq > 0:
                relevance_score = section_freq / baseline_freq
                if relevance_score > 1.5: # We only care about significantly over-represented roots
                    results[section_name][root] = relevance_score

    # Step 3: Print the results in a readable format
    print("\n--- Correlation Results: Top Keywords per Section ---")
    for section_name, keywords in results.items():
        # Sort keywords by their relevance score in descending order
        sorted_keywords = sorted(keywords.items(), key=lambda item: item[1], reverse=True)
        
        print(f"\n## Section: {section_name.upper()}")
        if not sorted_keywords:
            print("  No significant keywords found.")
            continue
            
        for i, (root, score) in enumerate(sorted_keywords[:5]): # Print top 5
            print(f"  {i+1}. Keyword: '{root}' (Relevance Score: {score:.2f})")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    analyze_correlations()