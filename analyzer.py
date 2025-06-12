#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from src.analyzer import ProjectAnalyzer
from src.claude_client import ClaudeClient
from src.utils.file_utils import save_response

def get_project_path():
    """Prompt user for project path and validate it."""
    while True:
        path = input("\nEnter the path to the project you want to analyze: ").strip()
        
        # Handle empty input
        if not path:
            print("Please enter a valid path.")
            continue
            
        # Convert to absolute path if relative
        if not os.path.isabs(path):
            path = os.path.abspath(path)
            
        # Validate path
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            continue
            
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory.")
            continue
            
        return path

def main():
    # Load environment variables
    load_dotenv()
    
    print("Project Analyzer")
    print("===============")
    print("This tool will analyze your project structure and get architectural insights from Claude AI.")
    
    # Get project path from user
    project_path = get_project_path()
    
    print(f"\nAnalyzing project at: {project_path}")
    
    # Initialize analyzer and process project
    analyzer = ProjectAnalyzer(project_path)
    project_summary = analyzer.analyze()
    
    # Save project summary
    analyzer.save_summary(project_summary)
    
    # Initialize Claude client and get analysis
    claude_client = ClaudeClient()
    analysis = claude_client.analyze_project(project_summary)
    
    # Print and save analysis
    print("\nClaude's Analysis:")
    print("=" * 80)
    print(analysis)
    print("=" * 80)
    
    # Save analysis to file
    save_response(analysis)

if __name__ == "__main__":
    main() 