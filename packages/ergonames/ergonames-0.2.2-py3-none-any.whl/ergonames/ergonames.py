import endpoints
import helpers

EXPLORER_API_URL = "https://api-testnet.ergoplatform.com/"

MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

def resolve_ergoname(name):
    name = reformat_name(name)
    tokenData = helpers.create_token_data(name)
    if tokenData != None:
        tokenArray = helpers.convert_token_data_to_token(tokenData)
        tokenId = helpers.get_asset_minted_at_address(tokenArray)
        tokenTransactions = endpoints.get_token_transaction_data(tokenId)
        tokenLastTransaction = helpers.get_last_transaction(tokenTransactions)
        tokenCurrentBoxId = helpers.get_box_id_from_transaction_data(tokenLastTransaction)
        address = endpoints.get_box_address(tokenCurrentBoxId)
        return address
    return None

def check_already_registered(name):
    name = reformat_name(name)
    address = resolve_ergoname(name)
    if address != None:
        return True
    return False

def reverse_search(address):
    tokenData = helpers.create_address_data(address)
    tokenArray = helpers.create_address_tokens_array(tokenData)
    tokenArray = helpers.remove_wrong_names_tokens(tokenArray)
    owned = helpers.check_correct_ownership(tokenArray, address)
    return owned

def get_total_amount_owned(address):
    owned = reverse_search(address)
    return len(owned)

def check_name_price(name):
    name = reformat_name(name)
    return None

def get_block_id_registered(name):
    name = reformat_name(name)
    tokenData = helpers.create_token_data(name)
    if tokenData != None:
        tokenArray = helpers.convert_token_data_to_token(tokenData)
        tokenId = helpers.get_asset_minted_at_address(tokenArray)
        tokenTransactions = endpoints.get_token_transaction_data(tokenId)
        tokenFirstTransactions = helpers.get_first_transaction(tokenTransactions)
        tokenMintBoxId = helpers.get_box_id_from_transaction_data(tokenFirstTransactions)
        tokenMintBox = endpoints.get_box_by_id(tokenMintBoxId)
        blockId = helpers.get_block_id_from_box_data(tokenMintBox)
        return blockId
    return None

def get_block_registered(name):
    name = reformat_name(name)
    tokenData = helpers.create_token_data(name)
    if tokenData != None:
        tokenArray = helpers.convert_token_data_to_token(tokenData)
        tokenId = helpers.get_asset_minted_at_address(tokenArray)
        tokenTransactions = endpoints.get_token_transaction_data(tokenId)
        tokenFirstTransactions = helpers.get_first_transaction(tokenTransactions)
        tokenMintBoxId = helpers.get_box_id_from_transaction_data(tokenFirstTransactions)
        tokenMintBox = endpoints.get_box_by_id(tokenMintBoxId)
        height = helpers.get_settlement_height_from_box_data(tokenMintBox)
        return height
    return None

def get_timestamp_registered(name):
    name = reformat_name(name)
    blockRegistered = get_block_id_registered(name)
    if blockRegistered != None:
        blockData = endpoints.get_block_by_block_height(blockRegistered)
        timestamp = helpers.get_timestamp_from_block_data(blockData)
        return timestamp
    return None

def get_date_registered(name):
    name = reformat_name(name)
    blockRegistered = get_block_id_registered(name)
    if blockRegistered != None:
        blockData = endpoints.get_block_by_block_height(blockRegistered)
        timestamp = helpers.get_timestamp_from_block_data(blockData)
        date = helpers.convert_timestamp_to_date(timestamp)
        return date
    return None

def reformat_name(name):
    name = name.lower()
    return name

def check_name_valid(name):
    for i in name:
        asciiCode = int(ord(i))
        if asciiCode <= 44:
            return False
        elif asciiCode == 47:
            return False
        elif asciiCode >= 58 and asciiCode <= 94:
            return False
        elif asciiCode == 96:
            return False
        elif asciiCode >= 123 and asciiCode <= 125:
            return False
        elif asciiCode >= 127:
            return False
    return True