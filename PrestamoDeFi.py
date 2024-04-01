from web3 import Web3
from eth_account import Account

from web3.exceptions import Web3Exception

# Intentar conectarse a la red de Ganache
try:
    ganache_url = "http://localhost:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    if not w3.is_connected():
        print("No se pudo conectar a Ganache. Asegúrate de que Ganache esté en funcionamiento.")
    exit()
except Exception as e:
    print(f"Error al intentar conectar con Ganache: {e}")
    exit()
    
print("Conectado a Ganache")

# Direccion del contrato inteligente desplegado
contract_address = "0xafcEc1e121a8a699013D6888ca4bd72306501E38" 
# Cambia por la dirección del contrato
# Direccion del socio principal
socio_principal_address = "0x52e142729398b60420F80d69690c2e1D92DD38bB"
# Cambia por la dirección del socio principal
# Clave privada del socio principal (necesaria para firmar transacciones)
socio_principal_private_key = "0x6be634001a55696e57b1bba7dba2e0c98f6e0a264b7fb63b6e0b867a74661cbc"


# Cambia por la clave privada del socio principal
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"clientes","outputs":[{"internalType":"bool","name":"activado","type":"bool"},{"internalType":"uint256","name":"saldoGarantia","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"empleadosPrestamista","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetalleDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct PrestamoDeFi.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Funcion para enviar transaccion:
def enviar_transaccion(w3, txn_dict, private_key):
    
    try:
        signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        return txn_receipt
    except Exception as e:
        # Lanzar la excepción para ser capturada por la función que llama
        raise Exception(f"Error al enviar la transacción: {e}")
# Funciones de interacción con el contrato

# Instanciar el contrato desplegado
contract_instance = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi']
)
# Función para dar de alta un prestamista por el socio principal
#def alta_prestamista(nuevo_prestamista_address):
#   try:
def alta_prestamista(nuevo_prestamista_address):
    try:
        txn_hash = contract_instance.functions.alta_prestamista(nuevo_prestamista_address).transact({'from': socio_principal_address})
        tx_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
        return tx_receipt.status
    except Exception as e:
        print(f"Error al ejecutar la transacción: {e}")
        return None
    
# Ejecutar la función
resultado = alta_prestamista(nuevo_prestamista_address)
if resultado == true:
    print("El prestamista fue agregado exitosamente.")
else:
    print("Hubo un problema al agregar el prestamista.")
    
# Función para registrar un nuevo cliente
def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    try:
        # Verificar si el cliente ya está registrado
        if contract_instance.functions.prestamistas(prestamista_address).call():
            return "El cliente ya está registrado"
        
        # Firmar la transacción
        nonce = w3.eth.getTransactionCount(prestamista_address)
        transaction = contract_instance.functions.alta_cliente(nuevo_cliente_address).buildTransaction({
            'from': prestamista_address,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.toWei('5000', 'wei')
        })
        signed_txn = w3.eth.account.signTransaction(transaction, prestamista_private_key)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        # Verificar el estado de la transacción
        if tx_receipt.status:
            return "Cliente registrado exitosamente"
        else:
            return "Error en la transacción"
    except Exception as e:
        print(f"Error al ejecutar la transacción: {e}")
        return 

# Ejecutar la función
resultado = alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key)
if resultado:
    print(resultado)

# Función para depositar garantía
def depositar_garantia(direccion_cliente, valor, clave_privada_cliente):
    try:
        # Preparar la transacción
        nonce = w3.eth.getTransactionCount(direccion_cliente)
        transaction = contract_instance.functions.depositarGarantia().buildTransaction({
            'from': direccion_cliente,
            'nonce': nonce,
            'value': w3.toWei(valor, 'ether'),
            'gas': 3000000,
            'gasPrice': w3.toWei('5000', 'wei')
        })
        
        # Firmar la transacción
        signed_txn = w3.eth.account.signTransaction(transaction, clave_privada_cliente)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        # Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return "Garantía depositada exitosamente"
        else:
            return "Error en la transacción"
    except Exception as e:
        print(f"Error al ejecutar la transacción: {e}")
        return None
    
# Ejecutar la función
resultado = depositar_garantia(cliente_address, monto_garantia, clave_privada_cliente)
if resultado:
    print(resultado)
    
# Función para solicitar un préstamo
def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        nonce = w3.eth.getTransactionCount(direccion_cliente)
        transaction = contract_instance.functions.solicitar_prestamo(direccion_cliente, monto, plazo).buildTransaction({
            'from': direccion_cliente,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.toWei('5000', 'wei')
        })
        signed_txn = w3.eth.account.signTransaction(transaction, clave_privada_cliente)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.events["PrestamoSolicitado"]["id"]
    except Exception as e:
        print(f"Error al solicitar el préstamo: {e}")
        return None
    
# Ejecutar la función
resultado = depositar_garantia(cliente_address, monto_garantia, clave_privada_cliente)
if resultado:
    print(resultado)
    
# Función para aprobar un préstamo
def aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Comprobar la validez del préstamo y del prestatario
        if not contract_instance.functions.prestamos(prestamo_id).aprobado():
            nonce = w3.eth.getTransactionCount(prestamista_address)
            transaction = contract_instance.functions.aprobar_prestamo(prestatario_address, prestamo_id).buildTransaction({
                'from': prestamista_address,
                'nonce': nonce,
                'gas': 3000000,
                'gasPrice': w3.toWei('5000', 'wei')
            })
            signed_txn = w3.eth.account.signTransaction(transaction, prestamista_private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            return tx_receipt
        else:
            return "El préstamo ya está aprobado"
    except Exception as e:
        print(f"Error al aprobar el préstamo: {e}")
        return None
    
# Ejecutar la función
resultado = aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key)
if resultado:
    print("El préstamo fue aprobado exitosamente.")

# Función para reembolsar un préstamo
def reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key):
    try:
        nonce = w3.eth.getTransactionCount(cliente_address)
        transaction = contract_instance.functions.reembolsar_prestamo(prestamo_id).buildTransaction({
            'from': cliente_address,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.toWei('5000', 'wei')
        })
        signed_txn = w3.eth.account.signTransaction(transaction, cliente_private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    except Exception as e:
        print(f"Error al reembolsar el préstamo: {e}")
        return None

# Ejecutar la función
resultado = reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key)
if resultado:
    print("El préstamo fue reembolsado exitosamente.")
    
# Función para liquidar la garantía de un préstamo
def liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key):
    try:
        nonce = w3.eth.getTransactionCount(prestamista_address)
        transaction = contract_instance.functions.liquidar_garantia(prestamo_id).buildTransaction({
            'from': prestamista_address,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.toWei('5000', 'wei')
        })
        signed_txn = w3.eth.account.signTransaction(transaction, prestamista_private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    except Exception as e:
        print(f"Error al liquidar la garantía: {e}")
        return None

# Ejecutar la función
resultado = liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key)
if resultado:
    print("La garantía ha sido liquidada exitosamente.")
    
    
# Instanciar contrato
contract = web3.eth.contract(address=contract_address, abi=abi)

# Función para obtener préstamos por prestatario
def obtener_prestamos_por_prestatario(prestatario_address):
    try:
        # Llamada al contrato para obtener la lista de IDs de préstamos del prestatario
        prestamos_ids = contract.functions.obtener_prestamos_por_prestatario(prestatario_address).call()
        return prestamos_ids
    except Exception as e:
        print(f"Error al obtener préstamos por prestatario: {e}")
        return None

# Ejecutar la función
resultado = obtener_prestamos_por_prestatario(prestatario_address)
if resultado:
    print("IDs de préstamos asociados al prestatario:", resultado)
else:
    print("Error al obtener los préstamos asociados al prestatario.")
    
    
# Función para obtener detalles de un préstamo por prestatario y ID
def obtener_detalle_de_prestamo(prestatario_address, prestamo_id):
    try:
        # Llamada al contrato para obtener los detalles del préstamo
        detalle_prestamo = contract.functions.obtener_detalle_de_prestamo(prestatario_address, prestamo_id).call()
        return detalle_prestamo
    except Exception as e:
        print(f"Error al obtener detalles de préstamo: {e}")
        return None

# Ejecutar la función
resultado = obtener_detalle_de_prestamo(prestatario_address, prestamo_id)
if resultado:
    print("Detalles del préstamo:")
    print("Cliente:", resultado[0])
    print("Monto:", resultado[1])
    print("Plazo:", resultado[2])
    print("Aprobado:", resultado[3])
    print("Reembolsado:", resultado[4])
else:
    print("Error al obtener detalles del préstamo.")