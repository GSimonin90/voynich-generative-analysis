import re
import os

# --- CONFIGURATION: Standard Voynich Manuscript Section Mapping ---
# This dictionary maps section names to the folio (page) numbers they contain.
# Folio numbers are represented as integers for easy comparison (e.g., 'f1r' -> 10, 'f1v' -> 11).
# We convert f[N]r to N*10 and f[N]v to N*10+1.
SECTION_MAP = {
    "botanical": (11, 571),       # f1v to f57v
    "astronomical": (670, 731),    # f67r to f73v
    "biological": (750, 841),      # f75r to f84v
    "pharmacological": (870, 1021), # f87r to f102v (some sources vary, this is a common range)
    "text_only": (1030, 1161)     # f103r to f116v
}

def get_folio_id(folio_str):
    """Converts a folio string like 'f1r' or 'f102v' into a unique integer."""
    match = re.match(r'f(\d+)([rv])', folio_str)
    if not match:
        return None
    page_num, side = match.groups()
    page_id = int(page_num) * 10
    if side == 'v':
        page_id += 1
    return page_id

def segment_manuscript(original_file="voynich.txt", output_dir="sections"):
    """
    Reads the original transcription file and segments it into thematic sections
    based on the folio markers.
    """
    print(f"--- Starting Manuscript Segmentation on '{original_file}' ---")
    
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: Original transcription file '{original_file}' not found.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"📂 Output directory set to '{output_dir}/'")

    # Use regex to find all folio markers and the text that follows them
    # This pattern captures the folio ID and all content until the next folio ID
    pages = re.split(r'(<f\d+[rv]>)', full_text)
    
    # Initialize dictionaries to hold the text for each section
    section_texts = {name: "" for name in SECTION_MAP.keys()}
    
    current_folio_id = None
    processed_pages = 0

    # The split gives us [text_before_first_marker, marker1, text1, marker2, text2, ...]
    # We iterate in pairs (marker, text)
    for i in range(1, len(pages), 2):
        marker = pages[i]
        text_content = pages[i+1]
        
        folio_str = marker.strip('<>')
        current_folio_id = get_folio_id(folio_str)
        
        if current_folio_id is None:
            continue
            
        # Clean the text content for this page (simple version)
        # This removes transcriber comments, line breaks, etc.
        cleaned_text = re.sub(r'\{.*?\}|\[.*?\]|\n', ' ', text_content) # Remove comments and newlines
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip() + ' ' # Consolidate whitespace
        
        # Find which section this page belongs to
        found_section = False
        for section_name, (start_id, end_id) in SECTION_MAP.items():
            if start_id <= current_folio_id <= end_id:
                section_texts[section_name] += cleaned_text
                found_section = True
                break
        
        if found_section:
            processed_pages += 1

    print(f"\nProcessed {processed_pages} pages from the manuscript.")

    # Save the concatenated text for each section into its own file
    for section_name, text in section_texts.items():
        if text:
            output_filename = os.path.join(output_dir, f"{section_name}.txt")
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(text.strip())
            print(f"✅ Section '{section_name}' saved to '{output_filename}' ({len(text.split())} words)")
        else:
            print(f"⚠️ Section '{section_name}' was empty.")

    print("\n--- Segmentation Complete ---")


if __name__ == "__main__":
    segment_manuscript()