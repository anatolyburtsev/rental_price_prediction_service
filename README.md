# Rental price prediction service
MLOPS project

# [High level design (link)](docs/HighLevelDesign.md)

# Setup
## Create virtual env
```shell
python -m venv .env
source .env/bin/activate
```

## Install dependencies
```shell
pip install -r requirements.txt
```

## Fetch data
### Example
```shell
python src/fetch_data.py --city vancouver-bc --output_prefix train_data --output_format csv
```

### Get help
```shell
python src/fetch_data.py --help
```