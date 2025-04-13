import os
import re

# File extensions to include
EXTENSIONS = ['.js', '.jsx', '.css']

# Files or folders to exclude (relative paths or names)
EXCLUDED_FILES = {
    'node_modules',
    'package-lock.json'
}

# Regex patterns for comments
single_line_comment = re.compile(r'//.*?$|(?<!:)//.*?$|^\s*//.*?$', re.MULTILINE)
multi_line_comment = re.compile(r'/\*.*?\*/', re.DOTALL)

def is_excluded(path):
    for exclude in EXCLUDED_FILES:
        if exclude in path.replace("\\", "/"):  # Normalize for Windows/Linux
            return True
    return False

def remove_comments_from_file(file_path):
    if is_excluded(file_path):
        print(f"Skipped (excluded): {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = re.sub(multi_line_comment, '', content)
        content = re.sub(single_line_comment, '', content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def walk_and_clean(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(subdir, file)
                if not is_excluded(full_path):
                    remove_comments_from_file(full_path)

if __name__ == "__main__":
    project_root = os.getcwd()
    walk_and_clean(project_root)
    print("✅ Finished comment removal.")
