import os
import json
from pathlib import Path

class ProjectAnalyzer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.ignored_dirs = {
            'node_modules', 'venv', '__pycache__', '.git', 
            'dist', 'build', '.pytest_cache', '.coverage',
            'target', '.idea', '.vscode', 'coverage'
        }
        self.ignored_extensions = {
            '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
            '.exe', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
            '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg',
            '.mp3', '.mp4', '.avi', '.mov', '.wav', '.pdf',
            '.zip', '.tar', '.gz', '.rar', '.7z'
        }
        self.max_lines_per_file = 150  # First 100 + last 50 lines
        self.max_file_size = 100 * 1024  # 100KB
        self.max_files = 1000  # Maximum number of files to analyze
        self.max_total_size = 50 * 1024 * 1024  # 50MB total content size
        self.current_total_size = 0
        self.file_count = 0
    
    def analyze(self):
        """Analyze the project and return a list of file summaries."""
        file_summaries = []
        dir_structure = self._get_directory_structure()
        
        print("\nAnalyzing project files...")
        print("This might take a while for large projects.")
        
        for file_path in self.project_root.rglob("*"):
            if self.file_count >= self.max_files:
                print(f"\nWarning: Reached maximum file limit ({self.max_files}). Some files will be skipped.")
                break
                
            if self.current_total_size >= self.max_total_size:
                print(f"\nWarning: Reached maximum content size limit ({self.max_total_size/1024/1024:.1f}MB). Some files will be skipped.")
                break
                
            if self._should_analyze_file(file_path):
                summary = self._analyze_file(file_path)
                if summary:
                    file_summaries.append(summary)
                    self.file_count += 1
                    self.current_total_size += len(summary['content'].encode('utf-8'))
                    
                    # Print progress every 50 files
                    if self.file_count % 50 == 0:
                        print(f"Analyzed {self.file_count} files...")
        
        print(f"\nAnalysis complete. Analyzed {self.file_count} files.")
        
        return {
            "directory_structure": dir_structure,
            "files": file_summaries,
            "analysis_limits": {
                "max_files": self.max_files,
                "max_total_size_mb": self.max_total_size/1024/1024,
                "files_analyzed": self.file_count,
                "total_size_mb": self.current_total_size/1024/1024
            }
        }
    
    def _should_analyze_file(self, file_path):
        """Check if a file should be analyzed."""
        if not file_path.is_file():
            return False
            
        # Skip ignored directories
        if any(ignored in file_path.parts for ignored in self.ignored_dirs):
            return False
            
        # Skip ignored extensions
        if file_path.suffix.lower() in self.ignored_extensions:
            return False
            
        # Skip large files
        if file_path.stat().st_size > self.max_file_size:
            return False
            
        return True
    
    def _get_directory_structure(self):
        """Get a tree representation of the directory structure."""
        structure = []
        
        def add_to_structure(path, level=0):
            if any(ignored in path.parts for ignored in self.ignored_dirs):
                return
                
            rel_path = path.relative_to(self.project_root)
            if path.is_dir():
                structure.append({
                    "type": "directory",
                    "path": str(rel_path),
                    "level": level
                })
                for child in path.iterdir():
                    add_to_structure(child, level + 1)
            else:
                if self._should_analyze_file(path):
                    structure.append({
                        "type": "file",
                        "path": str(rel_path),
                        "level": level
                    })
        
        add_to_structure(self.project_root)
        return structure
    
    def _analyze_file(self, file_path):
        """Analyze a single file and return its summary."""
        try:
            # Get relative path
            rel_path = str(file_path.relative_to(self.project_root))
            
            # Get extension
            extension = file_path.suffix
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Skip if first 10 lines are blank or comments
            first_lines = lines[:10]
            if all(line.strip() == '' or line.strip().startswith('#') for line in first_lines):
                return None
            
            # Count lines
            line_count = len(lines)
            
            # Get optimized content
            if line_count > self.max_lines_per_file:
                first_part = lines[:100]
                last_part = lines[-50:]
                middle_summary = f"\n... {line_count - 150} lines omitted ...\n"
                content = ''.join(first_part) + middle_summary + ''.join(last_part)
            else:
                content = ''.join(lines)
            
            return {
                "path": rel_path,
                "extension": extension,
                "line_count": line_count,
                "content": content
            }
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")
            return None
    
    def save_summary(self, summary):
        """Save the project summary to a JSON file."""
        output_path = self.project_root / "project_summary.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2) 