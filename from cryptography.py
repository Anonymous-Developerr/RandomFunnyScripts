from cryptography.fernet import Fernet
import json
import os

# Archivo donde se guardarán las contraseñas
PASSWORD_FILE = "passwords.json"
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def save_password(service, username, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}
    
    passwords[service] = {"username": username, "password": encrypted_password}
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)
    print("Contraseña guardada correctamente.")

def get_password(service):
    key = load_key()
    if not os.path.exists(PASSWORD_FILE):
        print("No hay contraseñas guardadas.")
        return None
    
    with open(PASSWORD_FILE, "r") as file:
        passwords = json.load(file)
    
    if service in passwords:
        encrypted_password = passwords[service]["password"]
        username = passwords[service]["username"]
        decrypted_password = decrypt_password(encrypted_password, key)
        return username, decrypted_password
    else:
        print("Servicio no encontrado.")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        print("1. Guardar contraseña")
        print("2. Obtener contraseña")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            servicio = input("Nombre del servicio: ")
            usuario = input("Nombre de usuario: ")
            contraseña = input("Contraseña: ")
            save_password(servicio, usuario, contraseña)
        elif opcion == "2":
            servicio = input("Nombre del servicio: ")
            resultado = get_password(servicio)
            if resultado:
                print(f"Usuario: {resultado[0]}\nContraseña: {resultado[1]}")
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")
            