import fat_py.fat2 as fat2
import fat_py.fat2.consts as consts
from factom_keys.fct import FactoidPrivateKey, FactoidAddress

from fat_py import FATd

fatd = FATd()

private_key = FactoidPrivateKey(key_string="Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK")
address = private_key.get_factoid_address()

output_addresses = [
    FactoidAddress(address_string="FA2ybgFNYQiZFgTjkwQwp74uGsEUHJc6hGEh4YA3ai7FcssemapP"),
    FactoidAddress(address_string="FA34L6m7rQypr5PVmKGJ1Y4FQ6gDWbVaA49kFTGn1sSVZj6D8pFJ"),
]

print(fatd.get_pegnet_balances(address))

tx = fat2.Transaction()
tx.set_input(address, "PEG", 1000)
tx.add_transfer(output_addresses[0], 500)
tx.add_transfer(output_addresses[1], 500)

tx_batch = fat2.TransactionBatch()
tx_batch.add_transaction(tx)
tx_batch.add_signer(private_key)
ext_ids, content = tx_batch.sign()

print(content.decode())
print(fatd.send_transaction(consts.TRANSACTIONS_CHAIN_ID, ext_ids, content))
