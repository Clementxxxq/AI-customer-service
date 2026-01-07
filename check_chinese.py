"""
Check for remaining Chinese characters in Python files
"""
import os
import re
from pathlib import Path

def has_chinese(text):
    """Check if text contains Chinese characters"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def check_directory(path, extensions=['.py']):
    """Recursively check all files with given extensions"""
    files_with_chinese = []
    
    for file_path in Path(path).rglob('*'):
        # Skip directories
        if file_path.is_dir():
            continue
        
        # Skip hidden and common ignore patterns
        if any(part.startswith('.') for part in file_path.parts):
            continue
        if '__pycache__' in file_path.parts:
            continue
        if 'docs' in file_path.parts:
            continue
            
        # Check file extension
        if not any(str(file_path).endswith(ext) for ext in extensions):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if has_chinese(content):
                    # Find lines with Chinese
                    lines_with_chinese = []
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if has_chinese(line):
                            lines_with_chinese.append((line_num, line.strip()))
                    
                    files_with_chinese.append((file_path, lines_with_chinese))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return files_with_chinese

if __name__ == "__main__":
    print("🔍 Checking for Chinese characters in Python files...")
    print("=" * 70)
    
    files = check_directory(".")
    
    if not files:
        print("✅ No Chinese characters found! All files are in English.")
    else:
        print(f"❌ Found {len(files)} file(s) with Chinese characters:\n")
        for file_path, lines in files:
            print(f"📄 {file_path}")
            for line_num, line_text in lines:
                print(f"   Line {line_num}: {line_text[:80]}")
            print()
    
    print("=" * 70)
