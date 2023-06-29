import os
import pandas as pd
from web3 import Web3, exceptions
import time
from datetime import datetime

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/Your-Infura-Project-Id'))

def get_transaction_receipt(tx_hash):
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except exceptions.TransactionNotFound:
        return None

def scan_ethereum_blockchain():
    if os.path.exists("last_scanned_block.txt"):
        with open("last_scanned_block.txt", "r") as file:
            start_block = int(file.read().strip())
    else:
        start_block = 0

    block = start_block

    while True:
        latest_block = w3.eth.block_number
        if latest_block > block:
            print(f"Scanning Blocks {block+1} to {latest_block}")
            data = []

            for b in range(block+1, latest_block + 1):
                block_data = w3.eth.get_block(b, full_transactions=True)
                for tx in block_data['transactions']:
                    if tx['to'] is None:
                        receipt = get_transaction_receipt(tx['hash'])
                        if receipt is not None:
                            contract_address = receipt['contractAddress']
                            timestamp = w3.eth.get_block(b)['timestamp']
                            timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                            data.append({
                                'block': b,
                                'from': tx['from'],
                                'contract_address': contract_address,
                                'timestamp': timestamp
                            })

            if data:
                print("Contract Creations:")
                for item in data:
                    print(f"Block: {item['block']}")
                    print(f"From: {item['from']}")
                    print(f"Contract Address: {item['contract_address']}")
                    print(f"Timestamp: {item['timestamp']}")
                    print("---------------------")

            block = latest_block

        time.sleep(10)

scan_ethereum_blockchain()
