# Bioinformatics Cell Analysis
## Run
### GitHub Codespaces
```bash
make setup
make pipeline
make dashboard
```

### Or run manually
```bash
pip install -r requirements.txt
python load_data.py
python analysis.py
streamlit run dashboard.py
```

## Database
The data from `cell-count.csv` is loaded into a SQLite database containing a single table called samples.

## Files
- `load_data.py` creates the SQLite database and imports the data.
- `analysis.py` generates the required tables, statistics, and plots.
- `dashboard.py` displays the analysis in a Streamlit dashboard.
