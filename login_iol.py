import requests
import time

# Configuración inicial
username = '' # Usuario
password = ''  # Contraseña
refresh_token = None  # Inicialmente, no tenemos un refresh token
access_token = None
token_expiration = 0  # Guardará el tiempo de expiración del token

def authenticate():
    global access_token, refresh_token, token_expiration
    
    url = "https://api.invertironline.com/token"
    data = {
        'username': username,
        'password': password,
        'grant_type': 'password'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        token_expiration = time.time() + 900  # Expira en 15 minutos
        print("Autenticación exitosa.")
    else:
        print(f"Error en la autenticación: {response.status_code} - {response.text}")

def refresh_access_token():
    global access_token, refresh_token, token_expiration
    
    url = "https://api.invertironline.com/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        token_expiration = time.time() + 900  # Renueva el tiempo de expiración
        print("Token de acceso renovado.")
    else:
        print(f"Error al renovar el token: {response.status_code} - {response.text}")

def get_headers():
    """
    Verifica si el token ha expirado y lo renueva si es necesario.
    Devuelve los headers con el token de acceso.
    """
    if time.time() > token_expiration:
        print("El token ha expirado, renovando...")
        refresh_access_token()

    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

def get_bonos():
    """
    Función para obtener las cotizaciones de bonos en Argentina.
    """
    url = "https://api.invertironline.com/api/v2/Cotizaciones/letra/argentina/Todos"
    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener cotizaciones: {response.status_code} - {response.text}")
        return None
    
def get_acciones():
    """
    Función para obtener las cotizaciones de acciones en Argentina.
    """
    url = "https://api.invertironline.com/api/v2/Cotizaciones/acciones/argentina/Todos"
    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener cotizaciones: {response.status_code} - {response.text}")
        return None
    
def get_opciones():
    """
    Función para obtener las cotizaciones de opciones en Argentina.
    """
    url = "https://api.invertironline.com/api/v2/Cotizaciones/opciones/argentina/Todos"
    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener cotizaciones: {response.status_code} - {response.text}")
        return None
