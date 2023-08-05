import requests
import math

EXPLORER_API_URL = "https://api-testnet.ergoplatform.com/"

MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

class Token:

    def __init__(self, id, boxId, name):
        self.id = id
        self.boxId = boxId
        self.name = name

def get_token_data(tokenName, limit, offset):
    url = EXPLORER_API_URL + "api/v1/tokens/search?query=" + str(tokenName) + "&limit=" + str(limit) + "&offset=" + str(offset)
    data = requests.get(url).json()
    return data

def create_token_data(tokenName):
    total = get_token_data(tokenName, 1, 0)['total']
    neededCalls = math.floor(total / 500) + 1
    tokenData = []
    offset = 0
    if total > 0:
        for i in range(neededCalls):
            data = get_token_data(tokenName, 500, offset)['items']
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

def get_box_address(boxId):
    url = EXPLORER_API_URL + "api/v1/boxes/" + (str(boxId))
    data = requests.get(url).json()
    return data['address']

def check_box_address(address):
    if address == MINT_ADDRESS:
        return True
    return False

def get_asset_minted_at_address(tokenArray):
    for i in tokenArray:
        address = get_box_address(i.boxId)
        if (check_box_address(address)):
            return i.id
    return None

def get_token_transaction_data(tokenId):
    total = get_max_transactions_for_token(tokenId)
    url = EXPLORER_API_URL + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1&offset=" + str(total-1)
    data = requests.get(url).json()['items']
    return data

def get_max_transactions_for_token(tokenId):
    url = EXPLORER_API_URL + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1"
    total = requests.get(url).json()['total']
    return total

def get_last_transaction(data):
    length = len(data)
    return data[length-1]

def get_box_id_from_transaction_data(data):
    return data['boxId']

def resolve_ergoname(name):
    tokenData = create_token_data(name)
    if tokenData != None:
        tokenArray = convert_token_data_to_token(tokenData)
        tokenId = get_asset_minted_at_address(tokenArray)
        tokenTransactions = get_token_transaction_data(tokenId)
        tokenLastTransaction = get_last_transaction(tokenTransactions)
        tokenCurrentBoxId = get_box_id_from_transaction_data(tokenLastTransaction)
        address = get_box_address(tokenCurrentBoxId)
        return address
    else:
        return None