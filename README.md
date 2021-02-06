# Introduction

coin-tracker-solution is used to check real-time data on coinbase and coinGecko and export multiple CSV files with a specific format.

## Requirement

python3, and installation of dependencies on requirements.txt

```bash
pip install -r requirements.txt
```

Remember to add key and secret

```python
coinbase = ccxt.coinbase(
    {
        'apiKey': '',
        'secret': '',
    })

```
and modify the rootPath
```python
rootPath = r"the directory you want to save output files"

```
Run
```bash
python coin-tracker-solution.py
```
Then enter the coin id you want to check
```bash
Please enter ID:BTC
Inital price is ....
or 
```
```bash
Please enter ID:BTC LTC
Inital price list is ....
