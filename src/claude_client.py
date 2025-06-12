import os
import json
import requests
import re

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")
        
        # Validate API key format
        if not self._validate_api_key(self.api_key):
            raise ValueError("Invalid Claude API key format")
        
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def _validate_api_key(self, api_key):
        """Validate Claude API key format."""
        # Claude API keys typically start with 'sk-' and are 40+ characters
        return bool(re.match(r'^sk-[a-zA-Z0-9]{40,}$', api_key))
    
    def analyze_project(self, project_summary):
        """Send project summary to Claude and get analysis."""
        # Sanitize project summary to remove any sensitive data
        sanitized_summary = self._sanitize_summary(project_summary)
        
        prompt = """Analyze this project structure and code. For large files, I've included first 100 and last 50 lines.

Key points to analyze:
1. Project purpose and main features
2. Major components and their interactions
3. Architectural issues or mismatches
4. Missing features or improvements needed
5. Top 3 priorities for next steps

"""
        prompt += json.dumps(sanitized_summary, indent=2)
        
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30  # Add timeout
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Claude API: {str(e)}")
            return "Error: Could not get analysis from Claude API"
    
    def _sanitize_summary(self, summary):
        """Remove potentially sensitive data from project summary."""
        if isinstance(summary, dict):
            return {k: self._sanitize_summary(v) for k, v in summary.items()}
        elif isinstance(summary, list):
            return [self._sanitize_summary(item) for item in summary]
        elif isinstance(summary, str):
            # Remove potential API keys, passwords, etc.
            return re.sub(r'(?i)(api[_-]?key|password|secret|token)[=:]\s*[^\s]+', '[REDACTED]', summary)
        return summary 