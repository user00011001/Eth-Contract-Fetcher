import os
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from web3 import Web3, exceptions

logging.basicConfig(level=logging.INFO)

# Connect to Ethereum mainnet via Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/177575bd62614fc69e6e60bec0e1867f'))

def get_block_number_by_timestamp(target_timestamp: int) -> int:
    current_block = w3.eth.block_number
    low, high = 0, current_block

    while low < high:
        mid = (low + high) // 2
        mid_block_time = w3.eth.get_block(mid).timestamp

        if mid_block_time < target_timestamp:
            low = mid + 1
        else:
            high = mid

    return low

def get_transaction_receipt(tx_hash: str) -> Optional[Dict]:
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except exceptions.TransactionNotFound as e:
        logging.error(f"Transaction not found: {e}")
        return None

def get_block_data(b: int) -> Dict:
    try:
        return w3.eth.get_block(b, full_transactions=True)
    except Exception as e:
        logging.error(f"Error while getting block data: {e}")
        return {}

def scan_blocks(block: int, latest_block: int) -> None:
    for b in range(block, latest_block + 1):
        block_data = get_block_data(b)
        for tx in block_data.get('transactions', []):
            if tx['to'] is None:
                receipt = get_transaction_receipt(tx['hash'])
                if receipt and receipt['contractAddress']:
                    timestamp = datetime.fromtimestamp(block_data['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"New Contract Creation Detected:")
                    logging.info(f"Block: {b}")
                    logging.info(f"From: {tx['from']}")
                    logging.info(f"Contract Address: {receipt['contractAddress']}")
                    logging.info(f"Timestamp: {timestamp}")
                    logging.info("---------------------")

def scan_ethereum_blockchain():
    twenty_four_hours_ago = int((datetime.now() - timedelta(days=1)).timestamp())
    start_block = get_block_number_by_timestamp(twenty_four_hours_ago)
    logging.info(f"Starting scan from block {start_block}")

    while True:
        latest_block = w3.eth.block_number
        if latest_block > start_block:
            logging.info(f"Scanning Blocks {start_block} to {latest_block}")
            scan_blocks(start_block, latest_block)
            start_block = latest_block + 1

        time.sleep(10)

scan_ethereum_blockchain()
