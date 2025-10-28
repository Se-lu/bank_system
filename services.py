from repositories import *
import hashlib

class AuthService:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_client(email, password):
        clients = ClientRepository.get_all_clients()
        for client in clients:
            if client.c_mail == email and client.c_password == AuthService.hash_password(password):
                return client
        return None

class BankingService:
    @staticmethod
    def transfer_funds(from_card, to_card, amount, description):
        # Check if cards exist
        from_card_obj = BankCardRepository.get_card_by_number(from_card)
        to_card_obj = BankCardRepository.get_card_by_number(to_card)
        
        if not from_card_obj or not to_card_obj:
            return False, "Invalid card numbers"
        
        # Create transaction
        transaction_data = {
            'from_card': from_card,
            'to_card': to_card,
            'amount': amount,
            'description': description
        }
        TransactionRepository.create_transaction(transaction_data)
        return True, "Transfer successful"

class PortfolioService:
    @staticmethod
    def get_client_portfolio(c_id):
        client = ClientRepository.get_client_by_id(c_id)
        cards = BankCardRepository.get_cards_by_client(c_id)
        transactions = TransactionRepository.get_client_transactions(c_id)
        
        return {
            'client': client,
            'bank_cards': cards,
            'recent_transactions': transactions
        }
