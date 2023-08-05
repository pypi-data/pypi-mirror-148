import math
import datetime

import endpoints
import ergonames

MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

class Token:

    def __init__(self, id, boxId, name):
        self.id = id
        self.boxId = boxId
        self.name = name

def create_address_data(address):
    tokens = endpoints.get_address_data(address)["tokens"]
    return tokens

def create_address_tokens_array(tokenData):
    tokenArray = []
    for i in tokenData:
        tk = Token(i['tokenId'], "none", i['name'])
        tokenArray.append(tk)
    return tokenArray

def remove_wrong_names_tokens(tokenArray):
    newArr = []
    for i in tokenArray:
        if i.name[0] == "~" and " " not in i.name:
            newArr.append(i)
    return newArr

def check_correct_ownership(tokenArray, address):
    ownedErgoNames = []
    for i in tokenArray:
        ownerAddress = ergonames.resolve_ergoname(i.name)
        if ownerAddress == address:
            ownedErgoNames.append(i)
    return ownedErgoNames

def create_token_data(tokenName):
    total = endpoints.get_token_data(tokenName, 1, 0)['total']
    neededCalls = math.floor(total / 500) + 1
    tokenData = []
    offset = 0
    if total > 0:
        for i in range(neededCalls):
            data = endpoints.get_token_data(tokenName, 500, offset)['items']
            tokenData += data
        return tokenData
    else:
        return None

def convert_token_data_to_token(data):
    tokenArray = []
    for i in data:
        tk = Token(i['id'], i['boxId'], i['name'])
        tokenArray.append(tk)
    return tokenArray

def check_box_address(address):
    if address == MINT_ADDRESS:
        return True
    return False

def get_asset_minted_at_address(tokenArray):
    for i in tokenArray:
        address = endpoints.get_box_address(i.boxId)
        if (check_box_address(address)):
            return i.id
    return None

def get_last_transaction(data):
    length = len(data)
    return data[length-1]

def get_first_transaction(data):
    return data[0]

def get_box_id_from_transaction_data(data):
    return data['boxId']

def get_settlement_height_from_box_data(data):
    return data['settlementHeight']

def get_block_id_from_box_data(data):
    return data['blockId']

def get_timestamp_from_block_data(data):
    return data["block"]["header"]["timestamp"]

def convert_timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp/1000.0)
    return date