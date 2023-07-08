import os
import pandas as pd
from web3 import Web3, exceptions
import time
from datetime import datetime

# Connect to Ethereum mainnet via Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/Your-Infura-Project-Id'))

# Function to get a transaction receipt using its hash
def get_transaction_receipt(tx_hash):
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except exceptions.TransactionNotFound:  # If the transaction cannot be found
        return None

# Function to scan the Ethereum blockchain
def scan_ethereum_blockchain():
    # If file exists, open it and read the last scanned block
    if os.path.exists("last_scanned_block.txt"):
        with open("last_scanned_block.txt", "r") as file:
            start_block = int(file.read().strip())
    else:
        start_block = 0  # Otherwise, start from block 0

    block = start_block

    while True:
        # Get the latest block number
        latest_block = w3.eth.block_number
        if latest_block > block:
            print(f"Scanning Blocks {block+1} to {latest_block}")
            data = []

            # Iterate over blocks
            for b in range(block+1, latest_block + 1):
                # Get block data with full transactions
                block_data = w3.eth.get_block(b, full_transactions=True)
                for tx in block_data['transactions']:
                    if tx['to'] is None:  # If the transaction is contract creation
                        receipt = get_transaction_receipt(tx['hash'])
                        if receipt is not None:
                            contract_address = receipt['contractAddress']
                            # Get timestamp and convert it to a readable format
                            timestamp = w3.eth.get_block(b)['timestamp']
                            timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                            # Append data
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

            block = latest_block  # Update the block number to the latest block

        time.sleep(10)  # Wait 10 seconds before checking again

# Call the function
scan_ethereum_blockchain()
