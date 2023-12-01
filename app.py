from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

# Inicialización de la base de datos en memoria
BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    minumero = request.args.get('minumero')
    cuenta = next((c for c in BD if c.numero == minumero), None)

    if cuenta:
        contactos = {numero: BD[int(numero)].nombre for numero in cuenta.contactos}
        return jsonify(contactos)
    else:
        return "Cuenta no encontrada", 404

@app.route('/billetera/pagar', methods=['POST'])
def realizar_pago():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))

    cuenta_origen = next((c for c in BD if c.numero == minumero), None)
    cuenta_destino = next((c for c in BD if c.numero == numerodestino), None)

    if cuenta_origen and cuenta_destino:
        if cuenta_origen.saldo >= valor:
            cuenta_origen.saldo -= valor
            cuenta_destino.saldo += valor
            fecha = datetime.now().strftime("%d/%m/%Y")
            cuenta_origen.historial.append(f"Pago realizado de {valor} a {cuenta_destino.nombre}. Realizado en {fecha}")
            cuenta_destino.historial.append(f"Pago recibido de {valor} de {cuenta_origen.nombre}. Realizado en {fecha}")
            return f"Transacción exitosa. Saldo actual de {cuenta_origen.nombre}: {cuenta_origen.saldo}"
        else:
            return "Saldo insuficiente", 400
    else:
        return "Cuenta no encontrada", 404

@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    minumero = request.args.get('minumero')
    cuenta = next((c for c in BD if c.numero == minumero), None)

    if cuenta:
        historial = [f"{operacion}" for operacion in cuenta.historial]
        return jsonify({"saldo": cuenta.saldo, "operaciones": historial})
    else:
        return "Cuenta no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
