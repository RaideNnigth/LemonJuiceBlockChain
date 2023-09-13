from datetime import datetime

from wallet.transactionInput import TransactionInput
from wallet.transactionOutput import TransactionOutput
from blockchain.lemonBlock import LemonBlock
from wallet.juiceWallet import JuiceWallet
from wallet.utils import import_private_key

import demo.initialize_wallets as initialize_wallet

# Students wallet
albert_wallet= JuiceWallet(initialize_wallet.alberth_wallet_public_key, 
                           import_private_key(initialize_wallet.alberth_wallet_private_key),
                           initialize_wallet.alberth_wallet_address)

bertrand_wallet= JuiceWallet(initialize_wallet.bertrand_wallet_public_key,
                             import_private_key(initialize_wallet.bertand_wallet_private_key),
                            initialize_wallet.bertrand_wallet_address)

camille_wallet= JuiceWallet(initialize_wallet.camille_wallet_public_key,
                            import_private_key(initialize_wallet.camille_wallet_private_key),
                            initialize_wallet.camille_wallet_address)

# University Wallet
university_wallet= JuiceWallet(initialize_wallet.university_wallet_public_key,
                                 import_private_key(initialize_wallet.university_wallet_private_key),
                                 initialize_wallet.university_wallet_address)

# Universitarie Restaurant Wallet
universitarie_restaurant_wallet= JuiceWallet(initialize_wallet.universal_restaurant_public_key,
                                                import_private_key(initialize_wallet.universal_restaurant_private_key),
                                                initialize_wallet.universitarie_restaurant_address)
# Burn Wallet
burn_wallet= JuiceWallet(initialize_wallet.burn_public_key,
                            import_private_key(initialize_wallet.burn_private_key),
                            initialize_wallet.burn_address)

def blockchain():

    # Initial Block ---- University Wallet anual budget
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="INITIAL_HASH",
                               output_index=0, public_key="INITIAL_HASH")
    output_0 = TransactionOutput(public_key_hash=university_wallet.lemonade_address,
                                 amount=696969)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    
    block_0 = LemonBlock(
        time_stamp=timestamp_0,
        transaction_data={"inputs": inputs, "outputs": outputs}
    )

    # University Wallet distribute budget to students
    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash=block_0.cryptografic_hash(),
                               output_index=0, public_key=university_wallet.public_key)
    input_1 = TransactionInput(transaction_hash=block_0.cryptografic_hash(),
                               output_index=1, public_key=university_wallet.public_key)
    input_2 = TransactionInput(transaction_hash=block_0.cryptografic_hash(),
                               output_index=2, public_key=university_wallet.public_key)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.lemonade_address,
                                 amount=1000)
    output_1 = TransactionOutput(public_key_hash=bertrand_wallet.lemonade_address,
                                 amount=1000)
    output_2 = TransactionOutput(public_key_hash=camille_wallet.lemonade_address,
                                 amount=1000)
    inputs = [input_0.to_json(), input_1.to_json(), input_2.to_json()]
    outputs = [output_0.to_json(), output_1.to_json(), output_2.to_json()]
    
    block_1 = LemonBlock(
        time_stamp=timestamp_1,
        transaction_data={"inputs": inputs, "outputs": outputs},
        previous_block=block_0
    )

    # Students use Lemon Coin to buy food at Universitarie Restaurant
    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=0, public_key=albert_wallet.public_key)
    input_1 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=1, public_key=bertrand_wallet.public_key)
    input_2 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                                 output_index=2, public_key=camille_wallet.public_key)
    output_0 = TransactionOutput(public_key_hash=universitarie_restaurant_wallet.lemonade_address,
                                 amount=20)
    output_1 = TransactionOutput(public_key_hash=universitarie_restaurant_wallet.lemonade_address,
                                    amount=20)
    output_2 = TransactionOutput(public_key_hash=universitarie_restaurant_wallet.lemonade_address,
                                    amount=20)
    inputs = [input_0.to_json(), input_1.to_json(), input_2.to_json()]
    outputs = [output_0.to_json(), output_1.to_json(), output_2.to_json()]
    block_2 = LemonBlock(
        time_stamp=timestamp_2,
        transaction_data={"inputs": inputs, "outputs": outputs},
        previous_block=block_1
    )

    # Universitarie Restaurant Burns Lemon Coin to reduce the amount of Lemon Coin in circulation and get money from the University
    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    input_0 = TransactionInput(transaction_hash=block_1.cryptografic_hash(),
                               output_index=0, public_key=universitarie_restaurant_wallet.public_key)
    output_0 = TransactionOutput(public_key_hash=burn_wallet.lemonade_address,
                                 amount=60)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_3 = LemonBlock(
        time_stamp=timestamp_3,
        transaction_data={"inputs": inputs, "outputs": outputs},
        previous_block=block_2
    )
    
    return block_3
