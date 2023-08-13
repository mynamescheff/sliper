from flask import Flask, render_template, request, jsonify
import os
from user_agents import parse

app = Flask(__name__)

SECRET_PASSWORD = ""

@app.route('/')
def index():
    user_agent_string = request.headers.get("User-Agent")
    user_agent = parse(user_agent_string)
    ip_address = request.remote_addr

    file_path = os.path.join(os.path.dirname(__file__), "devices.txt")
    with open(file_path, "a") as file:
        file.write(f"Device: {user_agent.device.family}, OS: {user_agent.os.family}, Browser: {user_agent.browser.family}, IP Address: {ip_address}\n")

    return render_template('index.html')

@app.route('/sleep', methods=['POST'])
def sleep():
    data = request.get_json()
    if 'password' in data and data['password'] == SECRET_PASSWORD:
        os.system('shutdown /h')
        return jsonify({'message': 'PC is going to sleep'})
    else:
        return jsonify({'message': 'Invalid password'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)