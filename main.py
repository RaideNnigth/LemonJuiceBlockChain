from datetime import datetime

from blockchain.lemonBlock import LemonBlock as Block
from blockchain.networkNodeClient import NetworkNodeClient as NodeTransaction
from wallet.transactionInput import TransactionInput
from wallet.transactionOutput import TransactionOutput
from wallet.utils import initialize_wallet
from wallet.transaction import Transaction


def test_given_valid_signature_when_validate_then_no_exception_is_thrown(blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.cryptografic_hash(), output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address, amount=5)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()

    transaction_data = transaction.send_to_nodes()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    node.validade()


def test_given_sender_tries_to_send_fund_from_somebody_else_when_validate_then_exception_is_thrown(
        blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.cryptografic_hash(), output_index=1)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address, amount=5)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction_data = transaction.send_to_nodes()
    transaction.sign()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    node.validade()


def test_given_amounts_dont_match_when_validate_then_exception_is_thrown(
        blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.cryptografic_hash(), output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address, amount=6)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction_data = transaction.send_to_nodes()
    transaction.sign()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    node.validade()
        
albert_wallet = initialize_wallet()
bertrand_wallet = initialize_wallet()
camille_wallet = initialize_wallet()


timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
input_0 = TransactionInput(transaction_hash="abcd1234",
                               output_index=0, public_key=albert_wallet.public_key)
output_0 = TransactionOutput(public_key_hash="Albert",
                                 amount=40)
inputs = [input_0.to_json()]
outputs = [output_0.to_json()]
block_0 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        time_stamp=timestamp_0
    )

timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
input_0 = TransactionInput(transaction_hash=block_0.cryptografic_hash(),
                               output_index=0)
output_0 = TransactionOutput(public_key_hash=bertrand_wallet.lemonade_address,
                                 amount=30)
output_1 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address,
                                 amount=10)
inputs = [input_0.to_json()]
outputs = [output_0.to_json(), output_1.to_json()]

block_1 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        time_stamp=timestamp_1,
        previous_block=block_0
    )

timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
input_0 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=1)
output_0 = TransactionOutput(public_key_hash=camille_wallet.lemonade_address,
                                 amount=10)
inputs = [input_0.to_json()]
outputs = [output_0.to_json()]
block_2 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        time_stamp=timestamp_2,
        previous_block=block_1
    )

timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
input_0 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=0)
output_0 = TransactionOutput(public_key_hash=camille_wallet.lemonade_address,
                                 amount=5)
output_1 = TransactionOutput(public_key_hash=bertrand_wallet.lemonade_address,
                                 amount=25)
inputs = [input_0.to_json()]
outputs = [output_0.to_json(), output_1.to_json()]
block_3 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        time_stamp=timestamp_3,
        previous_block=block_2
    )

blockchain = block_3

test_given_valid_signature_when_validate_then_no_exception_is_thrown(blockchain, albert_wallet, camille_wallet)
#test_given_sender_tries_to_send_fund_from_somebody_else_when_validate_then_exception_is_thrown(blockchain, albert_wallet, camille_wallet)
#test_given_amounts_dont_match_when_validate_then_exception_is_thrown(blockchain, albert_wallet, camille_wallet)
