# Create your models here.
from django.db import models
from cryptography.fernet import Fernet

from Crypto.Cipher import AES
import base64
import hashlib

PASSWORD = "941902019BamdadPass"
IV = "7418529639638521"

password = PASSWORD.encode('ascii')
cryptkey = hashlib.sha256(password).digest()
iv = IV.encode('ascii')


def decode(secretdata):
    secretdata = base64.b64decode(secretdata)
    decipher = AES.new(cryptkey, AES.MODE_CBC, iv)
    decoded = decipher.decrypt(secretdata)

    # Remove PKCS7 padding
    padding_length = decoded[-1]
    decoded = decoded[:-padding_length]

    return decoded.decode("utf-8")


def encode(cleardata):
    cleardata = cleardata.encode("utf-8")
    padder = AES.block_size - len(cleardata) % AES.block_size
    padded_data = cleardata + bytes([padder] * padder)
    encipher = AES.new(cryptkey, AES.MODE_CBC, iv)
    encoded = encipher.encrypt(padded_data)
    return base64.b64encode(encoded).decode("utf-8")


class EncryptedTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        decrypted_value = decode(value)
        return decrypted_value

    def to_python(self, value):
        if value is None:
            # value = value + "a"
            return value

        # cipher_suite = Fernet(self.get_key())
        # print("=================")
        # print(value)
        decrypted_value = encode(value)

        return decrypted_value

    # def value_to_string(self, obj):
    #     print("+++++++++++++++++========")
    def get_db_prep_save(self, value, connection):
        if not value:
            return value
        # cipher_suite = Fernet(self.get_key())
        encrypted_value = encode(value)
        return encrypted_value

    def get_key(self):
        # Replace this with your actual key generation logic
        # Make sure to keep the key secret and secure
        key = b'dULedlrF-T3jDO-Ba3MCr0lAjP60xvsGuzioJw-bVgk='
        return key


class EncryptedIntegerField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        # raise Exception(value)
        cipher_suite = Fernet(self.get_key())
        decrypted_value = cipher_suite.decrypt(value.encode()).decode()
        # print(decrypted_value)
        return int(decrypted_value)

    def to_python(self, value):
        if value is None:
            return value

        cipher_suite = Fernet(self.get_key())
        decrypted_value = cipher_suite.decrypt(value.encode()).decode()
        return int(decrypted_value)

    def get_db_prep_save(self, value, connection):
        if not value:
            return value
        cipher_suite = Fernet(self.get_key())
        encrypted_value = cipher_suite.encrypt(str(value).encode()).decode()
        return encrypted_value

    def get_key(self):
        # Replace this with your actual key generation logic
        # Make sure to keep the key secret and secure
        key = b'dULedlrF-T3jDO-Ba3MCr0lAjP60xvsGuzioJw-bVgk='
        return key


class EncryptedIntegerField2(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        cipher_suite = Fernet(self.get_key())
        decrypted_value = cipher_suite.decrypt(value.encode()).decode()
        return int(decrypted_value)

    def to_python(self, value):
        if value is None:
            return value

        cipher_suite = Fernet(self.get_key())
        decrypted_value = cipher_suite.decrypt(value.encode()).decode()
        return int(decrypted_value)

    def get_db_prep_save(self, value, connection):
        if not value:
            return value
        cipher_suite = Fernet(self.get_key())
        encrypted_value = cipher_suite.encrypt(str(value).encode()).decode()
        return encrypted_value

    def get_key(self):
        # Replace this with your actual key generation logic
        # Make sure to keep the key secret and secure
        key = b'dULedlrF-T3jDO-Ba3MCr0lAjP60xvsGuzioJw-bVgk='
        return key


class ProductNew(models.Model):
    title = EncryptedTextField(max_length=100, blank=True, null=True)
    content = EncryptedTextField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField(blank=False, null=False)
    price_new = EncryptedIntegerField(blank=False, null=False)
    more_detail = EncryptedTextField(max_length=100, blank=True, null=True)
    new_field = EncryptedTextField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.title

    @property
    def get_price(self):
        return True if self.price is not None else False


class Product(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField(blank=False, null=False)


class CompleteProduct(models.Model):
    complete_title = models.CharField(max_length=100, blank=True, null=True)
    the_product = models.ForeignKey(Product, on_delete=models.CASCADE)
