from web3 import Web3
import json
import os
from datetime import datetime
import hashlib

class BlockchainService:
    def __init__(self, provider_url="http://localhost:8545"):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = None
        self.private_key = None
        
    def connect(self):
        """Connect to blockchain and set up account"""
        try:
            # Check connection
            if not self.w3.is_connected():
                print("❌ Cannot connect to blockchain - is Ganache running?")
                return False
                
            # Get accounts from Ganache
            accounts = self.w3.eth.accounts
            if not accounts:
                print("❌ No accounts available")
                return False
                
            self.account = accounts[0]
            print(f"✅ Connected to blockchain. Using account: {self.account}")
            return True
            
        except Exception as e:
            print(f"❌ Blockchain connection failed: {e}")
            return False
    
    def register_product(self, product_data):
        """Register product on blockchain"""
        try:
            # Create product hash
            product_json = json.dumps(product_data, sort_keys=True)
            product_hash = hashlib.sha256(product_json.encode()).hexdigest()
            
            # Create transaction with product data
            transaction = {
                'from': self.account,
                'to': self.account,  # Self-transaction for demo
                'value': 0,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'data': self.w3.to_hex(text=product_json),
                'nonce': self.w3.eth.get_transaction_count(self.account)
            }
            
            # Send transaction
            tx_hash = self.w3.eth.send_transaction(transaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex(),
                'block_number': receipt['blockNumber'],
                'product_hash': product_hash,
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_product(self, transaction_hash):
        """Verify product exists on blockchain"""
        try:
            # Get transaction
            tx = self.w3.eth.get_transaction(transaction_hash)
            
            if not tx:
                return {'verified': False, 'error': 'Transaction not found'}
            
            # Get transaction receipt for confirmation
            receipt = self.w3.eth.get_transaction_receipt(transaction_hash)
            
            # Decode product data from transaction
            if tx['input'] and tx['input'] != '0x':
                try:
                    product_data = self.w3.to_text(tx['input'])
                    product_json = json.loads(product_data)
                except:
                    product_json = {'data': 'Product data stored on blockchain'}
            else:
                product_json = {'data': 'No product data'}
            
            return {
                'verified': True,
                'product_data': product_json,
                'block_number': receipt['blockNumber'],
                'timestamp': self.get_block_timestamp(receipt['blockNumber']),
                'gas_used': receipt['gasUsed'],
                'manufacturer': tx['from']
            }
            
        except Exception as e:
            return {'verified': False, 'error': str(e)}
    
    def get_block_timestamp(self, block_number):
        """Get timestamp of a block"""
        try:
            block = self.w3.eth.get_block(block_number)
            return block['timestamp']
        except:
            return None
    
    def get_balance(self, address=None):
        """Get account balance"""
        if not address:
            address = self.account
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except:
            return 0.0

# Global blockchain instance
blockchain = BlockchainService()