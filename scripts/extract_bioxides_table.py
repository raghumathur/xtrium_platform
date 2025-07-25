import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import numpy as np
from matplotlib.transforms import Affine2D

# Path to the CSV file
csv_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                        'assets', 'databases', 'materials_database_bioxides.csv')

# Read the CSV file
df = pd.read_csv(csv_file)

# Extract only the required columns
extracted_df = df[['Commercial Name', 'Canonical Name', 'Chemical Formula']]

# Create a figure and axis with appropriate size
fig, ax = plt.subplots(figsize=(12, 8))

# Hide axes
ax.axis('off')

# Create a table
table = ax.table(
    cellText=extracted_df.values,
    colLabels=extracted_df.columns,
    loc='center',
    cellLoc='center',
    colWidths=[0.3, 0.4, 0.3]
)

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)  # Adjust table size

# Add a title
plt.title('Bioxides Materials Database - Selected Columns', fontsize=16)

# Save as PDF
output_pdf = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                         'output', 'bioxides_table.pdf')

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

# Add watermark
fig.text(0.5, 0.5, 'XTRIUM', fontsize=80, color='gray', 
         ha='center', va='center', alpha=0.2, 
         rotation=45, transform=fig.transFigure)

# Save to PDF
with PdfPages(output_pdf) as pdf:
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"Table has been exported to PDF: {output_pdf}")

# Also save as CSV for convenience
output_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                         'output', 'bioxides_table.csv')
extracted_df.to_csv(output_csv, index=False)
print(f"Table has also been exported to CSV: {output_csv}")
