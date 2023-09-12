from flask import Flask, render_template, url_for, request

from blockchain.networkNodeClient import NetworkNodeClient, TransactionException
from blockchain.initialize_blockchain import blockchain
from blockchain.lemonBlock import LemonBlock

from wallet.utils import initialize_wallet
from wallet.juiceWallet import JuiceWallet
from wallet.transaction import Transaction
from wallet.transactionInput import TransactionInput
from wallet.transactionOutput import TransactionOutput
from wallet.utils import get_address_from_public_key, validate_pair_key, get_balance_from_address, import_private_key

from datetime import datetime

app = Flask(__name__)

host = "192.168.8.5" # Change to your IP address

blockchain_base = blockchain()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/wallet', methods=['GET', 'POST'])
def wallet_access():
    global blockchain_base  # Declare blockchain_base as global
    if request.method == 'POST':
        
        public_key = request.form['public_key']
        private_key = request.form['private_key']
             
        # Validade if public key and private key are not empty
        if (public_key is None or private_key is None):
            return "Login Failed, public key or private key empty", 400
        
        # Validade if public key and private key are a pair
        if (validate_pair_key(public_key, private_key) == False):
            return "Login Failed, Keys does not match", 400
                
        # Import private key to RSA object
        private_key_object = import_private_key(private_key)
        
        # returns for the user the wallet address and balance, and wallet object
        wallet = JuiceWallet(public_key, private_key_object, get_address_from_public_key(public_key))
        balance = get_balance_from_address(wallet.public_key, wallet.lemonade_address, blockchain_base)
        address = wallet.lemonade_address
        
        return render_template('wallet-access.html', wallet=wallet, balance=balance, address=address, public_key=public_key, private_key=private_key)
        
    else: 
        return render_template('wallet.html')
    
@app.route('/wallet-create', methods=['GET', 'POST'])
def wallet_creation():
    if request.method == 'POST':
        wallet, private_key = initialize_wallet()
        
        return render_template('wallet-create.html', private_key=private_key, public_key=wallet.public_key, address=wallet.lemonade_address)
    else:
        return render_template('wallet-create.html')

@app.route("/transactions", methods=['POST'])
def validate_transaction():
    global blockchain_base  # Declare blockchain_base as global
    if request.method == 'POST':
        
        private_key = request.form['private_key']
        public_key = request.form['public_key']
        address = request.form['address']
        amount = request.form['amount']
                
        owner = JuiceWallet(public_key, import_private_key(private_key), get_address_from_public_key(public_key))
        
        timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
        
        input_0 = TransactionInput(transaction_hash=blockchain_base.cryptografic_hash(),
                                output_index=0)
        
        output_0 = TransactionOutput(public_key_hash=address,
                                    amount=int(amount))
        
        transaction = Transaction(owner, [input_0], [output_0])
        transaction.process_transaction()
        transaction_data = transaction.send_to_nodes()
        
        try:
            node = NetworkNodeClient(blockchain_base)
            node.receive(transaction_data)
            node.validade()
        except TransactionException as transaction_exception:
            return f'{transaction_exception}', 40
        
        blockchain_base = LemonBlock(timestamp_0, transaction_data, blockchain_base)
        
        balance = get_balance_from_address(owner.public_key, owner.lemonade_address, blockchain_base)
        
        return render_template('wallet-access.html', wallet=owner, balance=balance, address=address, public_key=public_key, private_key=private_key)
    else:
        return "Transaction failed", 400

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host=host)
