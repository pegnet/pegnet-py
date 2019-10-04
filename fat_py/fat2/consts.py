from enum import Enum
from typing import Dict

TRANSACTIONS_CHAIN_ID = bytes.fromhex("cffce0f409ebba4ed236d49d89c70e4bd1f1367d86402a3363366683265a242d")

PNT = "PNT"
CURRENCY_ASSETS = {"USD", "EUR", "JPY", "GBP", "CAD", "CHF", "INR", "SGD", "CNY", "HKD", "KRW", "BRL", "PHP", "MXN"}
COMMODITY_ASSETS = {"XAU", "XAG", "XPD", "XPT"}
CRYPTO_ASSETS = {"XBT", "ETH", "LTC", "RVN", "XBC", "FCT", "BNB", "XLM", "ADA", "XMR", "DASH", "ZEC", "DCR"}
ALL_PEGGED_ASSETS = CURRENCY_ASSETS.union(COMMODITY_ASSETS).union(CRYPTO_ASSETS)
ALL_ASSETS = ALL_PEGGED_ASSETS.union({PNT})

ASSET_GRADING_ORDER = [
    "PNT",
    "USD",
    "EUR",
    "JPY",
    "GBP",
    "CAD",
    "CHF",
    "INR",
    "SGD",
    "CNY",
    "HKD",
    "KRW",
    "BRL",
    "PHP",
    "MXN",
    "XAU",
    "XAG",
    "XPD",
    "XPT",
    "XBT",
    "ETH",
    "LTC",
    "RVN",
    "XBC",
    "FCT",
    "BNB",
    "XLM",
    "ADA",
    "XMR",
    "DASH",
    "ZEC",
    "DCR",
]
