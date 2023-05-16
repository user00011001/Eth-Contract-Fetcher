import os
import pandas as pd
from web3 import Web3, exceptions
import time
from datetime import datetime

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(
    'https://mainnet.infura.io/v3/Your-Infura-Project-Id'))


def get_transaction_receipt(tx_hash):
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except exceptions.TransactionNotFound:
        return None


def scan_ethereum_blockchain():
    # Get the current block number
    end_block = w3.eth.block_number
    # Get the last scanned block from a file (if it exists)
    if os.path.exists("last_scanned_block.txt"):
        with open("last_scanned_block.txt", "r") as file:
            start_block = int(file.read().strip())
    else:
        start_block = end_block

    # Start scanning from the last scanned block
    block = start_block + 1

    while True:
        # Get the latest block number
        latest_block = w3.eth.block_number
        if latest_block > block:
            print(f"Scanning Blocks {block} to {latest_block}")
            data = []

            # Iterate through blocks to scan
            for b in range(block, latest_block + 1):
                # Get block data
                block_data = w3.eth.get_block(b, full_transactions=True)
                # Iterate through all transactions in the block
                for tx in block_data['transactions']:
                    # Check if it's a contract creation
                    if tx['to'] is None:
                        # Get transaction receipt to get the contract address
                        receipt = get_transaction_receipt(tx['hash'])
                        if receipt is not None:
                            contract_address = receipt['contractAddress']
                            timestamp = w3.eth.get_block(b)['timestamp']
                            timestamp = datetime.fromtimestamp(
                                timestamp).strftime("%Y-%m-%d %H:%M:%S")
                            # Append the contract creation to the data list
                            data.append({
                                'block': b,
                                'from': tx['from'],
                                'contract_address': contract_address,
                                'timestamp': timestamp
                            })

            # Save the last scanned block to a file
            with open("last_scanned_block.txt", "w") as file:
                file.write(str(latest_block))

            # If there are new contract creations, display the results
            if data:
                print("Contract Creations:")
                for item in data:
                    print(f"Block: {item['block']}")
                    print(f"From: {item['from']}")
                    print(f"Contract Address: {item['contract_address']}")
                    print(f"Timestamp: {item['timestamp']}")
                    print("---------------------")

            # Update the block variable to continue from the next block
            block = latest_block + 1

        # Sleep for a specific time interval (e.g., 10 seconds) before checking for new blocks again
        time.sleep(10)


# Start continuously scanning the Ethereum blockchain
scan_ethereum_blockchain()
