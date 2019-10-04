import fat_py.fat2 as fat2
import fat_py.fat2.consts as consts
from factom_keys.fct import FactoidPrivateKey

from fat_py import FATd

fatd = FATd()

private_key = FactoidPrivateKey(key_string="Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK")
address = private_key.get_factoid_address()

print(fatd.get_pegnet_balances(address))

tx = fat2.Transaction()
tx.set_input(address, "pFCT", 10000)
tx.conversion = "pUSD"

tx_batch = fat2.TransactionBatch()
tx_batch.add_transaction(tx)
tx_batch.add_signer(private_key)
ext_ids, content = tx_batch.sign()

print(content.decode())
print(fatd.send_transaction(consts.TRANSACTIONS_CHAIN_ID, ext_ids, content))
