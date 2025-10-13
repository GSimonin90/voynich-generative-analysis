import re
import os

def final_deep_cleaner(source_file: str, destination_file: str):
    """
    Performs a final, robust cleanup of the Voynich transcription file,
    removing all known metadata, comments, and special characters.
    """
    try:
        if not os.path.exists(source_file):
            print(f"❌ Error: Source file '{source_file}' not found.")
            return

        print(f"📖 Reading '{source_file}' for the final deep clean...")
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_text_lines = []
        for line in lines:
            # Skip lines that are entirely comments or empty
            if line.strip().startswith('#') or not line.strip():
                continue

            # Isolate the textual part of the line (everything after the first '>')
            try:
                text_part = line.split('>', 1)[1]
            except IndexError:
                # If a line has no '>', it might be a stray comment or error, skip it
                continue

            # --- AGGRESSIVE CLEANING RULES ---
            # Remove all bracketed content: [source], <tag>, {illegible}, (comment)
            cleaned_line = re.sub(r'\[.*?\]', '', text_part)
            cleaned_line = re.sub(r'<[^>]*>', '', cleaned_line)
            cleaned_line = re.sub(r'\{.*?\}', '', cleaned_line)
            cleaned_line = re.sub(r'\(.*?\)', '', cleaned_line)

            # Remove special characters used for notes or errors
            cleaned_line = re.sub(r'[!%$?\'*,]', '', cleaned_line)

            # Standardize word separators: replace dots with spaces
            cleaned_line = cleaned_line.replace('.', ' ')

            # Remove any resulting multiple spaces and strip whitespace from ends
            cleaned_line = re.sub(r'\s+', ' ', cleaned_line).strip()

            if cleaned_line:
                cleaned_text_lines.append(cleaned_line)

        # Join all cleaned lines into a single block of text
        final_text = "\n".join(cleaned_text_lines)

        with open(destination_file, 'w', encoding='utf-8') as f:
            f.write(final_text)

        print(f"✅ Final deep clean complete. File saved as '{destination_file}'.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Ensure you have the original 'voynich.txt' file
    final_deep_cleaner("voynich.txt", "voynich_super_pulito.txt")