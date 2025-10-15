import matplotlib.pyplot as plt
import os

# --- Data from Appendix A of the paper ---
# Planetary roots and their calculated lift scores
planetary_roots = {
    'kch': 2.60,
    'ol': 3.47,
    'ro': 2.08,
    'da': 2.28,
    'teo': 2.50
}
# Control root and its lift score
control_root = {'che': 1.05}

def generate_lift_score_chart():
    """
    Generates and saves a publication-quality bar chart of the Statistical Lift Scores.
    """
    print("--- Generating Statistical Lift Score Chart ---")

    # Prepare data for plotting
    all_labels = list(planetary_roots.keys()) + list(control_root.keys())
    planetary_labels = list(planetary_roots.keys())
    planetary_scores = list(planetary_roots.values())
    control_label = list(control_root.keys())[0]
    control_score = list(control_root.values())[0]

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the main planetary roots
    ax.bar(planetary_labels, planetary_scores, color='#008080', label='Planetary Roots')
    # Plot the control root in a different color to distinguish it
    ax.bar(control_label, control_score, color='grey', label='Neutral Control Root')

    # Add a horizontal line at y=1.0 to represent the baseline
    # Anything above this line has a positive correlation.
    ax.axhline(y=1.0, color='r', linestyle='--', linewidth=1.5, label='Baseline (No Correlation)')

    # Add titles and labels for clarity
    ax.set_title('Statistical Lift Score of Planetary Roots in Zodiacal Contexts', fontsize=16)
    ax.set_xlabel('Core Root', fontsize=12)
    ax.set_ylabel('Statistical Lift Score', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.set_ylim(bottom=0, top=max(planetary_scores) * 1.15) # Set y-axis limit

    # Add the legend to explain the colors and the baseline
    ax.legend()

    # Create the 'charts' directory if it doesn't exist
    output_dir = 'charts'
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = os.path.join(output_dir, "lift_score_chart.png")
    
    # Save the figure in high resolution
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    
    print(f"✅ Chart successfully saved to '{output_filename}'")

if __name__ == "__main__":
    generate_lift_score_chart()