import spacy
from rake_nltk import Rake
import os
import argparse
import glob
from typing import List


# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Function to extract keywords from the text
def extract_keywords_from_text(text, num_keywords=10)->List[str]:
    """
    Extract top N entities from the input text.
    """
    doc = nlp(text)

    # Named Entity Recognition
    ner_keywords = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE', 'PRODUCT']]

    # RAKE keyword extraction
    rake = Rake()
    rake.extract_keywords_from_text(text)
    rake_keywords = rake.get_ranked_phrases()

    # Combine the lists and convert to lowercase
    all_keywords = ner_keywords + rake_keywords
    lowercase_keywords = [keyword.lower() for keyword in all_keywords]

    # Remove duplicates and preserve the original capitalization
    seen = set()
    unique_keywords = []
    for keyword, lowercase_keyword in zip(all_keywords, lowercase_keywords):
        if lowercase_keyword not in seen:
            seen.add(lowercase_keyword)
            unique_keywords.append(keyword)

    # Sort by length to prioritize longer phrases
    unique_keywords.sort(key=len, reverse=True)

    return unique_keywords[:num_keywords]


def process_text_file(input_file, num_keywords=10, output_file=None):
    """
    Read text from the input file; Extract top N entities from the text; Save the entities into an output file.
    If output_file is not specified, the default output file name is the same a input_file, but with a file extension `.keywords`.
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract keywords
    keywords = extract_keywords_from_text(text, num_keywords)

    # Generate output file name if not provided
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.keywords'

    # Write keywords to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for keyword in keywords:
            f.write(keyword + '\n')

    print(f'Keywords saved to: {output_file}')


def process_input_path(input_path, num_keywords=10):
    """
    Identify all files matching the input path pattern. For each matched file, extract entities from the file.
    """
    # Get all matching files in the input path
    matching_files = glob.glob(input_path)

    # Process each file
    for input_file in matching_files:
        process_text_file(input_file, num_keywords=num_keywords)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract keywords from a text file or a directory of text files.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_file', help='The input text file.')
    group.add_argument('-p', '--input_path', help='The input path with a pattern to match text files (e.g., "input/*.txt").')
    parser.add_argument('-o', '--output_file', help='The output file for the extracted keywords (optional).', default=None)
    parser.add_argument('-n', '--max_keyword_number', help='Number of keywords to be extracted (optional).', default=12)
    args = parser.parse_args()

    # Process the input file or input path and save extracted keywords to the output file
    if args.input_file:
        process_text_file(args.input_file, output_file=args.output_file, num_keywords=args.max_keyword_number)
    elif args.input_path:
        process_input_path(args.input_path, num_keywords=args.max_keyword_number)
