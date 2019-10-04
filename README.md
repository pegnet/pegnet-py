# fat-py

Kinda ugly, very alpha.

## Usage

```
>>> import fat_py
>>> fatd = fat_py.FATd()
>>> fatd.get_sync_status()
{'syncheight': 62, 'factomheight': 62}
```

Get PegNet Balances
```
>>> import fat_py
>>> from factom_keys.fct import FactoidAddress
>>> fatd = fat_py.FATd()
>>> address = FactoidAddress(address_string="FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q")
>>> fatd.get_pegnet_balances(address)
{'PEG': 0, 'pADA': 0, 'pBNB': 0, 'pBRL': 0, 'pCAD': 0, 'pCHF': 0, 'pCNY': 0, 'pDAS': 0, 'pDCR': 0, 'pETH': 0, 'pEUR': 0, 'pFCT': 0, 'pGBP': 0, 'pHKD': 0, 'pINR': 0, 'pJPY': 0, 'pKRW': 0, 'pLTC': 0, 'pMXN': 0, 'pPHP': 0, 'pRVN': 0, 'pSGD': 0, 'pUSD': 0, 'pXAG': 0, 'pXAU': 0, 'pXBC': 0, 'pXBT': 0, 'pXLM': 0, 'pXMR': 0, 'pZEC': 0}
```
