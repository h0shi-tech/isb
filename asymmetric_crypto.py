from cryptography.hazmat.primitives.asymmetric import rsa
import config

class AsymmetricCrypto:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """Генерация пары ключей RSA"""
        config_data = config.load_config()
        self.private_key = rsa.generate_private_key(
            public_exponent=config_data['asymmetric']['public_exponent'],
            key_size=config_data['asymmetric']['key_size']
        )
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key

    def encrypt(self, data):
        """Шифрование данных открытым ключом RSA"""
        return self.public_key.encrypt(
            data,
            config.get_rsa_padding()
        )

    def decrypt(self, encrypted_data):
        """Дешифрование данных закрытым ключом RSA"""
        return self.private_key.decrypt(
            encrypted_data,
            config.get_rsa_padding()
        ) 
