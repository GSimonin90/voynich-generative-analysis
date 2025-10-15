import re

# --- CONFIGURATION ---
KEYWORD_TO_MAP = 'ro'  # The root we want to investigate
TARGET_SECTION_FOLIOS = range(67, 74) # Folios for the Astronomical section (f67r to f73v)
TRANSCRIPTION_FILE = "voynich.txt"

def map_keyword_locations(keyword, target_folios, filename):
    """
    Searches the original transcription for a keyword and maps its exact locations
    (folio and line number) within a specific section.
    """
    print(f"--- Mapping all occurrences of the root '{keyword}' in the Astronomical Section ---")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ ERROR: Original transcription file '{filename}' not found.")
        return

    current_folio = None
    current_folio_num = 0
    found_count = 0
    
    # We create a simple regex to find the keyword as a whole word or part of a word.
    # \b matches word boundaries, so this would find 'ro' but not 'oro'.
    # For Voynich, it's better to find it anywhere.
    keyword_regex = re.compile(r'\b\w*' + re.escape(keyword) + r'\w*\b')

    print(f"Searching for words containing '{keyword}' in folios f{target_folios.start} to f{target_folios.stop-1}...")
    print("-" * 30)

    for i, line in enumerate(lines):
        # Check for folio markers like <f67r>
        folio_match = re.search(r'<f(\d+)[rv]>', line)
        if folio_match:
            current_folio = line.strip()
            current_folio_num = int(folio_match.group(1))

        if current_folio_num not in target_folios:
            continue

        # Search for the keyword in the current line
        matches = keyword_regex.findall(line)
        if matches:
            line_num = i + 1
            # Clean up the line for printing by removing comments
            clean_line = re.sub(r'\{.*?\}|\[.*?\]', '', line).strip()
            
            # Highlight the found words
            highlighted_line = clean_line
            for match in set(matches):
                highlighted_line = highlighted_line.replace(match, f"**{match}**")

            print(f"Location: {current_folio}, Line: {line_num}")
            print(f"  Context: {highlighted_line}")
            print("-" * 10)
            found_count += len(matches)

    print(f"\n--- Mapping Complete ---")
    print(f"✅ Found {found_count} total occurrences of words containing '{keyword}' in the target section.")

if __name__ == "__main__":
    map_keyword_locations(KEYWORD_TO_MAP, TARGET_SECTION_FOLIOS, TRANSCRIPTION_FILE)