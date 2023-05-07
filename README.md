# Entity Extraction from Articles

This script extracts entities from articles.


1. Use a Python virtual environment and install dependencies.

```
pip install -r requirements.txt
```

2. Install required NTLK modules.

```
python nltk-downloads.py
```

3. Check out the script inputs.

```
python main.py -h
```

4. Run the script with either an input file or an input path pattern.

```
python main.py -i "./data/article-keppel.txt"
python main.py -p "/home/ubuntu/environment/keywords-from-articles/data/*.txt"
```
