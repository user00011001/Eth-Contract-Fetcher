import os
import logging
from typing import Dict, List, Optional
from web3 import Web3, exceptions
from datetime import datetime
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to Ethereum mainnet via Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/Your-Infura-Project-Id'))

def get_transaction_receipt(tx_hash: str) -> Optional[Dict]:
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except exceptions.TransactionNotFound as e:
        logging.error(f"Transaction not found: {e}")
        return None

def get_start_block() -> int:
    if os.path.exists("last_scanned_block.txt"):
        with open("last_scanned_block.txt", "r") as file:
            return int(file.read().strip())
    else:
        return 0  # Otherwise, start from block 0

def get_block_data(b: int) -> Dict:
    try:
        return w3.eth.get_block(b, full_transactions=True)
    except Exception as e:
        logging.error(f"Error while getting block data: {e}")
        return {}

def get_timestamp(b: int) -> str:
    timestamp = get_block_data(b)['timestamp']
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def scan_blocks(block: int, latest_block: int) -> List[Dict]:
    data = []
    for b in range(block+1, latest_block + 1):
        block_data = get_block_data(b)
        for tx in block_data.get('transactions', []):
            if tx['to'] is None:  # If the transaction is contract creation
                receipt = get_transaction_receipt(tx['hash'])
                if receipt is not None:
                    contract_address = receipt['contractAddress']
                    timestamp = get_timestamp(b)
                    data.append({
                        'block': b,
                        'from': tx['from'],
                        'contract_address': contract_address,
                        'timestamp': timestamp
                    })
    return data

def scan_ethereum_blockchain():
    block = get_start_block()

    while True:
        latest_block = w3.eth.block_number
        if latest_block > block:
            logging.info(f"Scanning Blocks {block+1} to {latest_block}")
            data = scan_blocks(block, latest_block)

            if data:
                logging.info("Contract Creations:")
                for item in data:
                    logging.info(f"Block: {item['block']}")
                    logging.info(f"From: {item['from']}")
                    logging.info(f"Contract Address: {item['contract_address']}")
                    logging.info(f"Timestamp: {item['timestamp']}")
                    logging.info("---------------------")

            block = latest_block

        time.sleep(10)

# Call the function
scan_ethereum_blockchain()
