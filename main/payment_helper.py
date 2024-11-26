PAYLOVAPIKEY = 'JYVhflEK.paste_given_api_key_here'
BASEURL = 'BASE_URL/'

import requests

class PaylovHelper:

    @staticmethod
    def card_create(card_number, expiry, user_id):

        headers = {
            'API-KEY': PAYLOVAPIKEY
        }

        payload = {
            'userId': str(user_id),
            'cardNumber': card_number,
            'expireDate': expiry
        }

        url = BASEURL + 'merchant/userCard/createUserCard/'
        response = requests.post(url=url, headers=headers, json=payload)
        
        return response.json
    
    @staticmethod
    def confirm_card_create(card_id, otp):
        headers = {
            'API-KEY': PAYLOVAPIKEY
        }

        payload = {
            'cardId': card_id,
            'otp': otp
        }

        url = BASEURL + 'merchant/userCard/confirmUserCardCreate/'

        response = requests.post(url=url, headers=headers, json=payload)

        return response.json()
    
    @staticmethod
    def delete_user_card(user_card_id):

        headers = {
            'API-KEY': PAYLOVAPIKEY
        }

        

        url = BASEURL + f'merchant/userCard/deleteUserCard/?userCardId={user_card_id}'

        response = requests.delete(url=url, headers=headers)

        return response.json()
    
    @staticmethod
    def get_all_user_cards(user_id):
        
        headers = {
            'API-KEY': PAYLOVAPIKEY
        }
        
        url = BASEURL + f'merchant/userCard//getAllUserCards/?userId={user_id}'
        
        response = requests.get(url=url, headers=headers)
        
        return response.json()
            

    @staticmethod
    def create_payment_transaction(amount, user_id=None, account=None):
        
        headers = {
            'API-KEY': PAYLOVAPIKEY
        }
        
        payload = {
            "amount": amount,
            "userId": user_id or "",
            "account": account or {}
        }
        
        url = BASEURL + 'merchant/receipts/create/'
        
        response = requests.post(url=url, headers=headers, json=payload)
        
        return response.json()
    
    @staticmethod
    def confirm_payment(transaction_id, card_id, user_id):
      
        headers = {
            'API-KEY': PAYLOVAPIKEY
        }
        
        payload = {
            "transactionId": transaction_id,
            "cardId": card_id,
            "userId": user_id
        }
        
        url = BASEURL + 'merchant/receipts/pay/'
        
        response = requests.post(url=url, headers=headers, json=payload)
        
        return response.json()




# def get_test():
#     response = requests.get('http://127.0.0.1:8000/api/products')
#     return response.json()

