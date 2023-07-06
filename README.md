## Eth Contract Fetcher

A simple Python script to continuously scan the Ethereum blockchain for new contract creations.

### Requirements
- Python 3.6 or above
- Web3 Python library
- An Infura project ID

### Features
- Scans the Ethereum blockchain for newly created contracts
- Displays the block number, sender's address, contract address, and timestamp of each contract creation

### How to Run
1. Download the `contract_data.py` file to your computer.
2. Open a terminal.
3. Navigate to the directory containing the `contract_data.py` file.
4. Replace `'Your-Infura-Project-Id'` in the `contract_data.py` script with your actual Infura project ID.
5. Run the following command to start fetching data:

```bash
python3 contract_data.py
```

The script will start scanning the Ethereum blockchain for new contract creations continuously until manually stopped. 
