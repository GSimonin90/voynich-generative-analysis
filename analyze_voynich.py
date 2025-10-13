import math
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
        
        visualize_frequencies(word_counts, file_input)

        # ---- Advanced Structural Analysis ----
        print("\n--- 🔬 Structural Analysis ---")

        # 1. Entropy
        char_counts = Counter(text_without_spaces)
        text_length = len(text_without_spaces)
        entropy = -sum((c / text_length) * math.log2(c / text_length) for c in char_counts.values())
        print(f"\n💡 Entropy (per character): {entropy:.4f} bits")
        print("(Reference: Original ≈ 4.3, English ≈ 4.1)")

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
    """Creates and saves a bar chart of the most frequent words."""
    print(f"\n📊 Creating chart for '{filename}'...")
    try:
        common_words = word_counts.most_common(top_n)
        labels, values = zip(*common_words)

        plt.figure(figsize=(16, 9))
        plt.bar(labels, values, color='teal')
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title(f"Top {top_n} Most Frequent Words in '{filename}'")
        plt.xticks(rotation=60, ha='right')
        plt.tight_layout()
        
        chart_name = f"frequency_chart_{filename.replace('.txt', '')}.png"
        plt.savefig(chart_name)
        print(f"✅ Chart saved as '{chart_name}'")
        plt.show()
    except Exception as e:
        print(f"❌ Charting error: {e}")

if __name__ == "__main__":
    # Analyze each file you are interested in
    files_to_analyze = [
        "voynich_super_clean.txt",
        "generated_clean_normal_temp.txt",
        "generated_clean_low_temp.txt",
        "generated_clean_high_temp.txt"
    ]
    for file in files_to_analyze:
        full_analysis(file)