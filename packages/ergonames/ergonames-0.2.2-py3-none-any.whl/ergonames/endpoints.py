import requests

EXPLORER_API_URL = "https://api-testnet.ergoplatform.com/"

def get_address_data(address):
    url = EXPLORER_API_URL + "api/v1/addresses/" + str(address) + "/balance/confirmed"
    data = requests.get(url).json()
    return data

def get_token_data(tokenName, limit, offset):
    url = EXPLORER_API_URL + "api/v1/tokens/search?query=" + str(tokenName) + "&limit=" + str(limit) + "&offset=" + str(offset)
    data = requests.get(url).json()
    return data

def get_box_address(boxId):
    url = EXPLORER_API_URL + "api/v1/boxes/" + (str(boxId))
    data = requests.get(url).json()
    return data['address']

def get_token_transaction_data(tokenId):
    total = get_max_transactions_for_token(tokenId)
    url = EXPLORER_API_URL + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1&offset=" + str(total-1)
    data = requests.get(url).json()['items']
    return data

def get_max_transactions_for_token(tokenId):
    url = EXPLORER_API_URL + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1"
    total = requests.get(url).json()['total']
    return total

def get_box_by_id(boxId):
    url = EXPLORER_API_URL + "api/v1/boxes/" + str(boxId)
    data = requests.get(url).json()
    return data

def get_block_by_block_height(height):
    url = EXPLORER_API_URL + "api/v1/blocks/" + str(height)
    data = requests.get(url).json()
    return data