#!/bin/bash

# ==============================================================================
# AI Context Generator Script
#
# Description:
# This script creates a single text file (`ai_context.txt`) containing the
# directory tree and the contents of all relevant source code files in the
# current project directory. This is ideal for providing context to an AI model.
#
# Instructions:
# 1. Place this script in the root directory of your project.
# 2. Make it executable: chmod +x create_ai_context.sh
# 3. Run it: ./create_ai_context.sh
# 4. The `ai_context.txt` file will be created in the same directory.
# ==============================================================================

# --- Configuration ---

# The name of the output file.
OUTPUT_FILE="ai_context.txt"

# Directories to ignore completely in both the tree and file content.
# Use a pipe-separated string for the `tree` command's -I flag.
# Use an array for the `find` command.
IGNORE_DIRS_TREE="node_modules|.git|dist|build|vendor|__pycache__|.venv|.idea|.vscode|$OUTPUT_FILE"
IGNORE_DIRS_FIND=("node_modules" ".git" "dist" "build" "vendor" "__pycache__" ".venv" ".idea" ".vscode")

# File extensions to include. Add or remove extensions based on your project.
# This is a "whitelist" approach to avoid including binary files.
INCLUDE_EXTENSIONS=(
  "js" "jsx" "ts" "tsx" "html" "css" "scss" "sass" "less"
  "py" "rb" "php" "go" "java" "c" "cpp" "h" "hpp" "cs"
  "json" "yml" "yaml" "xml" "md" "sql" "puml" "py" "md" "txt"
  "Dockerfile" "docker-compose.yml" "package.json" "tsconfig.json" ".env.example"
)

# --- Script Logic ---

# Let the user know the script has started.
echo "🚀 Starting AI context generation..."

# Clear the output file if it already exists.
> "$OUTPUT_FILE"

# 1. Add a header to the output file.
{
  echo "================================================="
  echo "PROJECT CONTEXT FOR AI ANALYSIS"
  echo "================================================="
  echo "This document contains the project structure and source code for review."
  echo "Project root: $(pwd)"
  echo "Generated on: $(date)"
  echo ""
  echo "-------------------------------------------------"
  echo "PROJECT FILE AND FOLDER STRUCTURE"
  echo "-------------------------------------------------"
  echo ""
} >> "$OUTPUT_FILE"

# 2. Generate and append the directory tree.
# We use `tree` if it's available, otherwise we provide a message.
if command -v tree &> /dev/null
then
  echo "🌳 Generating file tree..."
  tree -a -I "$IGNORE_DIRS_TREE" >> "$OUTPUT_FILE"
else
  echo "⚠️ 'tree' command not found. Skipping directory tree generation." >> "$OUTPUT_FILE"
  echo "    For a better context, please install 'tree' (e.g., 'sudo apt-get install tree' or 'brew install tree')." >> "$OUTPUT_FILE"
fi

# 3. Add a separator before the code files.
{
  echo ""
  echo ""
  echo "-------------------------------------------------"
  echo "PROJECT SOURCE CODE FILES"
  echo "-------------------------------------------------"
  echo ""
} >> "$OUTPUT_FILE"

# 4. Prepare the `find` command arguments.
# This part constructs the `find` command to locate all desired files while
# excluding the ignored directories.

# Build the ignore directory part for `find`
find_ignore_paths=()
for dir in "${IGNORE_DIRS_FIND[@]}"; do
  find_ignore_paths+=(-o -path "./$dir/*")
done

# Build the include file part for `find`
find_include_files=()
for ext in "${INCLUDE_EXTENSIONS[@]}"; do
  # Handle exact filenames like 'Dockerfile' differently from extensions like '*.js'
  if [[ "$ext" == *.* ]] || [[ "$ext" == "Dockerfile" ]]; then
    find_include_files+=(-o -name "$ext")
  else
    find_include_files+=(-o -name "*.$ext")
  fi
done

echo "🔍 Finding and processing source files..."

# Find and process all relevant files
# The `-print0` and `read -r -d ''` combination handles files with spaces.
find . -type f \( "${find_ignore_paths[@]:1}" \) -prune -o \( "${find_include_files[@]:1}" \) -print0 | while IFS= read -r -d '' file; do

  # Get the file extension to use as a language hint for the markdown block.
  extension="${file##*.}"
  lang_hint="${extension,,}" # Convert to lowercase

  # Refine language hint for common cases
  case "$lang_hint" in
    js|jsx) lang_hint="javascript" ;;
    ts|tsx) lang_hint="typescript" ;;
    puml|plantuml) lang_hint="plantuml" ;;
    py) lang_hint="python" ;;
    rb) lang_hint="ruby" ;;
    md) lang_hint="markdown" ;;
    yml) lang_hint="yaml" ;;
  esac

  echo "  -> Processing: $file"

  # Append file header and content to the output file
  {
    echo "========================================="
    echo "FILE: ${file#./}" # Print file path without the leading ./
    echo "========================================="
    echo "\`\`\`${lang_hint}"
    cat "$file"
    echo "" # Ensure a newline before the closing backticks
    echo "\`\`\`"
    echo ""
    echo ""
  } >> "$OUTPUT_FILE"

done

echo "✅ Success! Context saved to '$OUTPUT_FILE'."
echo "➡️  You can now copy the contents of this file into the AI prompt."
