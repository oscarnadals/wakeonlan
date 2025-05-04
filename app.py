# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from pam import pam
import subprocess, socket, json, os
import paramiko

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_FILE = 'pcs.json'

def autenticar_usuario(user, pwd):
    return pam().authenticate(user, pwd)

def cargar_pcs():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return {}
    with open(DB_FILE) as f:
        return json.load(f)

def guardar_pcs(pcs):
    with open(DB_FILE, 'w') as f:
        json.dump(pcs, f, indent=2)

def hacer_ping(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def probar_ssh(ip, user='pi'):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, timeout=3)
        client.close()
        return True
    except Exception as e:
        return str(e)

def estado_pc(ip):
    if not hacer_ping(ip):
        return "Apagado"
    ssh_resultado = probar_ssh(ip)
    if ssh_resultado is True:
        return "Activo"
    elif "timed out" in str(ssh_resultado):
        return "Mantenimiento"
    else:
        return f"Error: {ssh_resultado}"

def enviar_paquete_wol(mac):
    mac = mac.replace(':', '').replace('-', '')
    data = bytes.fromhex('FF' * 6 + mac * 16)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(data, ('<broadcast>', 9))
    print(f"[WOL] Paquete enviado a {mac}")

def encender_con_esp(ip_esp):
    try:
        print(f"[ESP] Enviando POST a http://{ip_esp}/power")
        result = subprocess.run(
            ['curl', '-X', 'POST', f'http://{ip_esp}/power'],
            timeout=2, capture_output=True
        )
        if result.returncode != 0:
            raise Exception(f"Curl fallo con codigo {result.returncode}")
        print(f"[ESP] Respuesta del ESP32: {result.stdout.decode().strip()}")
    except Exception as e:
        raise Exception(f"No se pudo contactar con el ESP32: {e}")


@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if autenticar_usuario(user, pwd):
            session['usuario'] = user
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Usuario o pass incorrectos")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    pcs = cargar_pcs()

    if request.method == 'POST':
        accion = request.form['accion']
        nombre = request.form['nombre']

        if accion == 'Anadir':
            ip = request.form['ip']
            tipo = request.form.get('tipo', 'wol')
            pcs[nombre] = {'ip': ip, 'tipo': tipo}

            if tipo == 'wol':
                pcs[nombre]['mac'] = request.form['mac']
            elif tipo == 'esp':
                pcs[nombre]['esp_ip'] = request.form['esp_ip']

        elif accion == 'Eliminar' and nombre in pcs:
            pcs.pop(nombre)

        elif accion == 'Encender' and nombre in pcs:
            try:
                tipo = pcs[nombre].get("tipo", "wol")
                if tipo == "wol":
                    enviar_paquete_wol(pcs[nombre]['mac'])
                elif tipo == "esp":
                    encender_con_esp(pcs[nombre]['esp_ip'])
            except Exception as e:
                pcs[nombre]['error'] = str(e)
                print(f"[ERROR] {nombre}: {e}")

        guardar_pcs(pcs)

    estados = {nombre: estado_pc(data['ip']) for nombre, data in pcs.items()}
    return render_template('dashboard.html', pcs=pcs, estados=estados)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
