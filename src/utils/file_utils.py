import os
from datetime import datetime
from pathlib import Path

def save_response(response_text):
    """Save Claude's response to a file in the analysis folder."""
    # Create analysis directory if it doesn't exist
    analysis_dir = Path("analysis")
    analysis_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"claude_analysis_{timestamp}.txt"
    
    # Save response
    output_path = analysis_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response_text)
    
    print(f"\nAnalysis saved to: {output_path}") 