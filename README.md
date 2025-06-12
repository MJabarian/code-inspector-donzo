# Claude-Based Code Inspector – Donzo Edition


A Python CLI tool that analyzes your codebase and uses Claude AI to provide architectural insights — part of the Donzo automation suite. The tool provides a comprehensive analysis of your codebase, identifying architectural patterns, potential issues, and suggesting improvements.

## Features

- **Smart Project Scanning**:
  - Recursively scans project files
  - Ignores binary files, media files, and generated files
  - Skips common directories (node_modules, venv, etc.)
  - Handles large projects efficiently

- **Optimized Analysis**:
  - For large files: analyzes first 100 and last 50 lines
  - For small files: analyzes full content
  - Generates complete directory structure
  - Tracks file relationships and dependencies

- **Claude AI Integration**:
  - Sends optimized project summary to Claude
  - Gets detailed architectural analysis
  - Identifies potential issues and improvements
  - Suggests next steps

- **Output and Storage**:
  - Generates structured JSON summary
  - Saves analysis with timestamps
  - Provides clear progress indicators
  - Includes analysis limits and statistics

## Project Structure

```
code_inspector_donzo/
├── analyzer.py              # Main entry point
├── requirements.txt         # Project dependencies
├── README.md               # This file
└── src/
    ├── __init__.py         # Package initialization
    ├── analyzer.py         # Core analysis logic
    ├── claude_client.py    # Claude API integration
    └── utils/
        └── file_utils.py   # File operations
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Claude API key:
```
CLAUDE_API_KEY=your_api_key_here
```

## Usage

Run the analyzer:
```bash
python analyzer.py
```

The tool will:
1. Prompt you for the project path
2. Scan and analyze the project
3. Generate a `project_summary.json`
4. Send the summary to Claude
5. Print the analysis to console
6. Save the analysis in the `analysis` folder

## Analysis Limits

The tool includes safeguards for large projects:
- Maximum 1000 files analyzed
- Maximum 50MB total content size
- Files larger than 100KB are skipped
- Large files are truncated (first 100 + last 50 lines)

## Output Files

- `project_summary.json`: Contains:
  - Complete directory structure
  - File summaries with content
  - Analysis limits and statistics

- `analysis/claude_analysis_*.txt`: Contains:
  - Project purpose and features
  - Component analysis
  - Architectural issues
  - Missing features
  - Next steps

## Ignored Files and Directories

The tool automatically skips:
- Binary files (.exe, .dll, etc.)
- Media files (.jpg, .mp4, etc.)
- Generated files (.pyc, __pycache__, etc.)
- Common directories (node_modules, venv, etc.)
- Large files (>100KB)

## Requirements

- Python 3.6+
- Claude API key
- Required packages:
  - python-dotenv==1.0.0
  - requests==2.31.0

## Error Handling

The tool includes robust error handling:
- Validates project path
- Handles file reading errors
- Manages API communication issues
- Provides clear error messages

## Contributing

Feel free to submit issues and enhancement requests! 