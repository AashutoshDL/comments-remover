import os
import re

EXTENSIONS = ['.js', '.jsx']
EXCLUDED_FILES = {'node_modules', 'build'}

# Load AI-generated comment list
def load_ai_comments(file_path='ai_comments.txt'):
    if not os.path.exists(file_path):
        print(f"❌ Could not find {file_path}")
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

AI_COMMENTS = load_ai_comments()

def is_excluded(path):
    return any(excluded in path.replace("\\", "/") for excluded in EXCLUDED_FILES)

def remove_matched_comments(content):
    lines = content.splitlines()
    cleaned_lines = []

    block_comment = False
    block_buffer = []

    for line in lines:
        stripped = line.strip()

        # Handle multi-line block comments
        if '/*' in stripped:
            block_comment = True
            block_buffer = [stripped]
            if '*/' in stripped:
                block_comment = False
                if ' '.join(block_buffer) in AI_COMMENTS:
                    continue  # Remove full line comment
                cleaned_lines.append(line)
            continue

        if block_comment:
            block_buffer.append(stripped)
            if '*/' in stripped:
                block_comment = False
                combined = ' '.join(block_buffer)
                if combined in AI_COMMENTS:
                    continue
                cleaned_lines.extend(block_buffer)
            continue

        # Remove matching single-line comments
        if stripped.startswith('//') and stripped in AI_COMMENTS:
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def remove_comments_from_file(file_path):
    if is_excluded(file_path):
        print(f"⏭️  Skipped (excluded): {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = remove_matched_comments(content)

        if cleaned != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"🧹 Cleaned: {file_path}")
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def walk_and_clean(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(subdir, file)
                remove_comments_from_file(full_path)

if __name__ == "__main__":
    project_root = os.getcwd()
    walk_and_clean(project_root)
    print("✅ Finished cleaning matching AI comments.")
