from datetime import datetime

from wallet.transactionInput import TransactionInput
from wallet.transactionOutput import TransactionOutput
from blockchain.lemonBlock import LemonBlock

from wallet.utils import initialize_wallet

albert_wallet = initialize_wallet()
bertrand_wallet = initialize_wallet()
camille_wallet = initialize_wallet()

def get_wallets():
    print("-----------------------------------------------------------------------")
    albert_wallet.print_wallet()
    print("-----------------------------------------------------------------------")
    bertrand_wallet.print_wallet()
    print("-----------------------------------------------------------------------")
    camille_wallet.print_wallet()
    print("-----------------------------------------------------------------------")

def blockchain():
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="INITIAL_HASH",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address,
                                 amount=40)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_0 = LemonBlock(
        time_stamp=timestamp_0,
        transaction_data={"inputs": inputs, "outputs": outputs}
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

    block_1 = LemonBlock(
        time_stamp=timestamp_1,
        transaction_data={"inputs": inputs, "outputs": outputs},
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=1)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.lemonade_address,
                                 amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_2 = LemonBlock(
        time_stamp=timestamp_2,
        transaction_data={"inputs": inputs, "outputs": outputs},
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
    block_3 = LemonBlock(
        time_stamp=timestamp_3,
        transaction_data={"inputs": inputs, "outputs": outputs},
        previous_block=block_2
    )
    
    get_wallets()
    
    
    return block_3
