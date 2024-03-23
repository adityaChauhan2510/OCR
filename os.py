import os
import pytesseract
from PIL import Image
import collections

def ocr_directory(directory_path):
  """
  Performs OCR on all PDF files in a given directory and generates statistics.

  Args:
      directory_path: The path to the directory containing PDFs.

  Returns:
      A dictionary containing the following statistics:
          total_files: Total number of files processed (including non-PDFs).
          total_directories: Total number of subdirectories encountered.
          word_counts: A dictionary mapping words (case-insensitive) to their
                       total count and the number of files they appeared in.
  """

  total_files = 0
  total_directories = 0
  word_counts = collections.Counter()

  for root, dirs, files in os.walk(directory_path):
    total_directories += len(dirs)

    for filename in files:
      total_files += 1
      file_path = os.path.join(root, filename)

      if not filename.endswith(".pdf"):
        continue  # Skip non-PDF files

      try:
        # Use PyMuPDF for more reliable PDF handling (optional)
        # import fitz  # Install PyMuPDF if desired

        # with fitz.open(file_path) as doc:
        #   for page in doc:
        #     text = page.get_text("text")
        #     word_counts.update(process_text(text.lower()))  # Case-insensitive

        # Use textract for simpler extraction (potential limitations for complex PDFs)
        text = pytesseract.image_to_string(Image.open(file_path))
        word_counts.update(process_text(text.lower()))  # Case-insensitive
      except Exception as e:
        print(f"Error processing file {filename}: {e}")

  return {
      "total_files": total_files,
      "total_directories": total_directories,
      "word_counts": word_counts,
  }

def process_text(text):
  """
  Preprocesses text for word counting (e.g., removing punctuation).

  Args:
      text: The text string to process.

  Returns:
      A list of lowercase words (punctuation removed).
  """
  words = [word.strip().lower() for word in text.split() if word.isalnum()]
  return words

def sort_word_counts(word_counts):
  """
  Sorts word counts based on desired criteria.

  Args:
      word_counts: A dictionary mapping words to their counts.

  Returns:
      A list of tuples (word, count, num_files) sorted accordingly.
  """
  # Combine word, total count, and number of files for sorting
  data = [(word, word_counts[word][0], word_counts[word][1]) for word in word_counts]

  # Sort using a custom sorting key that prioritizes lowercase words
  # then sorts by number of files (ascending) and total count (descending)
  def sort_key(item):
    return (item[0].islower(), item[2], item[1], item[0])  # Lowercase first
  data.sort(key=sort_key)

  return data

if __name__ == "__main__":
  directory_path = "path/to/your/directory"  # Replace with your directory path
  results = ocr_directory(directory_path)

  print("Total files:", results["total_files"])
  print("Total directories:", results["total_directories"])

  print("\nList of words (sorted):")
  sorted_word_counts = sort_word_counts(results["word_counts"])
  for word, count, num_files in sorted_word_counts:
    print(f"{word:<10} {count:>6}   {num_files:>4}")