# Extract Sources From HTML Files

This simple scripts extracts to a CSV file all the sources included in the html files found at the directory and subdirectories specified by the user.

## How to run the script

1. If using virtual envs, create it and activate it.
2. Then install dependencies:
```bash
pip install -r requirements.txt
```
3. Then run the script specifying the parent directory to look for html files.
```
python main.py <your directory>
```