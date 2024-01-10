# Proper Noun Capitalization

Capitalize proper nouns in english sentences.

Provided dictionary `proper_nouns.json` is extracted from two corpus: Gutenberg project, Wikipedia-dump, which include 8 billion words.

# Create a proper noun dictionary from your own text files (Optional)

## Step 1

Gather all words from text files.

`python gather_dictionary.py ${DICTIONARY_SAVEPATH} ${TEXT_1} ${TEXT_2} ...`

## Step 2

Refinement phase.

1. Limit the length of keys
1. Limit the number of keys
1. Filter low-scored keys

`python refine_dictionary.py ${DIC_PATH} ${SAVE_PATH}`

# Capitalize text

## Step 1 (Optional)

Custom your own function in `capitalize.py`: `extract_target`, `envelop_target`

These are used for handling various format of text files.

## Step 2

Capitalize proper nouns in target text.

`python capitalize.py ${DIC_PATH} ${TARGET_PATH} ${SAVE_PATH}`