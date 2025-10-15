import math
import os
from collections import Counter
import matplotlib.pyplot as plt

def full_analysis(file_input: str):
    """
    Performs a complete statistical and structural analysis on a text file.
    """
    print(f"\n--- 🔬 Starting Full Analysis on '{file_input}' ---")
    try:
        with open(file_input, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        words = full_text.split()
        if not words:
            print("❌ File is empty.")
            return

        text_without_spaces = "".join(words)

        # ---- Basic Statistics ----
        print("\n--- 📊 General Statistics ---")
        print(f"Total number of words: {len(words)}")
        print(f"Number of unique words (vocabulary): {len(set(words))}")
        print(f"Average word length: {sum(len(p) for p in words) / len(words):.2f} characters")

        # ---- Word Frequency and Visualization ----
        word_counts = Counter(words)
        print("\n--- 🏆 Top 20 Most Common Words ---")
        for word, count in word_counts.most_common(20):
            print(f"{word:<15} | {count} times")
        
        # Call the updated visualization function
        visualize_frequencies(word_counts, file_input)

        # ---- Advanced Structural Analysis ----
        print("\n--- 🔬 Structural Analysis ---")

        # 1. Entropy
        char_counts = Counter(text_without_spaces)
        text_length = len(text_without_spaces)
        entropy = -sum((c / text_length) * math.log2(c / text_length) for c in char_counts.values())
        print(f"\n💡 Entropy (per character): {entropy:.4f} bits")

        # 2. Positional Analysis
        starts = Counter(p[0] for p in words if p)
        ends = Counter(p[-1] for p in words if p)
        print("\n🗺️ Most common STARTING characters:", [f"'{c}'" for c, _ in starts.most_common(5)])
        print("🗺️ Most common ENDING characters:  ", [f"'{c}'" for c, _ in ends.most_common(5)])
        
        # 3. Word Bigrams
        bigrams = zip(words, words[1:])
        bigram_counts = Counter(bigrams)
        print("\n🔗 Top 10 Most Common Word Pairs (Bigrams):")
        for (p1, p2), count in bigram_counts.most_common(10):
            print(f"'{p1} {p2}': {count} times")

        print("\n" + "="*53)
        print(f"--- ✅ Analysis of '{file_input}' Complete ---")

    except FileNotFoundError:
        print(f"❌ Error: File '{file_input}' not found.")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

def visualize_frequencies(word_counts: Counter, filename: str, top_n: int = 25):
    """Creates and saves a publication-quality bar chart of the most frequent words."""
    print(f"\n📊 Creating chart for '{filename}'...")
    
    # Dictionary to define plot details for each specific file
    plot_details = {
        "voynich_super_clean.txt": {
            "title": 'Word Frequency Distribution (Original "Super-Clean" Text)',
            "filename": "charts/frequency_chart_voynich_super_clean.png"
        },
        "generated_clean_normal_temp.txt": {
            "title": 'Word Frequency Distribution (Generated Text, Temp 0.7)',
            "filename": "charts/frequency_chart_generated_clean_normal_temp.png"
        },
        "generated_clean_low_temp.txt": {
            "title": 'Word Frequency Distribution (Generated Text, Temp 0.5)',
            "filename": "charts/frequency_chart_generated_clean_low_temp.png"
        },
        "generated_clean_high_temp.txt": {
            "title": 'Word Frequency Distribution (Generated Text, Temp 1.2)',
            "filename": "charts/frequency_chart_generated_clean_high_temp.png"
        }
    }
    
    # Fallback for any other filename
    details = plot_details.get(filename, {
        "title": f"Top {top_n} Words in {filename}",
        "filename": f"charts/frequency_chart_{filename.replace('.txt', '')}.png"
    })

    try:
        # Create the 'charts' directory if it doesn't exist
        os.makedirs('charts', exist_ok=True)
        
        common_words = word_counts.most_common(top_n)
        labels, values = zip(*common_words)

        plt.figure(figsize=(12, 7)) # Optimized figure size for a paper
        plt.bar(labels, values, color='#008080') # A darker teal color
        
        # Improved labels and title for clarity
        plt.title(details["title"], fontsize=16)
        plt.xlabel(f"Top {top_n} Most Frequent Words", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        
        plt.xticks(rotation=45, ha='right') # Rotate labels for readability
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a grid for better readability
        
        plt.tight_layout() # Ensure everything fits without being clipped
        
        # Save the figure in high resolution for publication quality
        chart_name = details["filename"]
        plt.savefig(chart_name, dpi=300) 
        
        print(f"✅ Chart saved as '{chart_name}'")
        plt.close() # Close the plot to free up memory

    except Exception as e:
        print(f"❌ Charting error: {e}")

if __name__ == "__main__":
    files_to_analyze = [
        "voynich_super_clean.txt",
        "generated_clean_normal_temp.txt",
        "generated_clean_low_temp.txt",
        "generated_clean_high_temp.txt"
    ]
    for file in files_to_analyze:
        full_analysis(file)