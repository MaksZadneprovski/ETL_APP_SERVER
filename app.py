import os

from flask import Flask, request, jsonify, render_template
from database import init_db, save_report, get_report, save_structure, get_structure, validate_credentials_db, \
    get_all_users, create_user, delete_user, get_all_structures
from models import Report, Structure

app = Flask(__name__)

#python -m venv venv
#source venv/bin/activate
#pip install -r requirements.txt

@app.route('/')
def index():
    return render_template('users.html')


@app.route('/saveReport', methods=['POST'])
def save_report_endpoint():
    report_id = request.args.get('reportId')
    report_json = request.data.decode('utf-8')
    save_report(report_id, report_json)

    os.makedirs('reports', exist_ok=True)

    with open(f"reports/{report_id}.txt", "w", encoding="utf-8") as file:
        file.write(report_json)

    return '', 200


@app.route('/getReport', methods=['GET'])
def get_report_endpoint():
    reportId = request.args.get('reportId')
    report_json = get_report(reportId)
    return report_json if report_json else '', 200


@app.route('/saveStructure', methods=['POST'])
def save_structure_endpoint():
    engineer_id = request.args.get('engineerId')
    structure_json = request.data.decode('utf-8')
    save_structure(engineer_id, structure_json)
    return '', 200


@app.route('/getStructure', methods=['GET'])
def get_structure_endpoint():
    engineer_id = request.args.get('engineerId')
    structure_json = get_structure(engineer_id)
    return structure_json if structure_json else '', 200

@app.route('/getAllStructures', methods=['GET'])
def get_all_structures_endpoint():
    # Получаем десериализованные структуры
    structures = get_all_structures()
    # Используем jsonify для возврата JSON
    return jsonify(structures), 200


@app.route('/validateCredentials', methods=['POST'])
def validate_credentials():
    login = request.args.get('login')
    password = request.args.get('password')
    credentials = validate_credentials_db(login, password)

    if credentials["is_valid"]:
        return jsonify({"message": "credentials are valid", "is_admin": credentials["is_admin"]}), 200
    else:
        return jsonify({"message": "credentials are invalid"}), 401


@app.route('/users', methods=['GET'])
def get_users_endpoint():
    users = get_all_users()
    return jsonify(users), 200


@app.route('/user', methods=['POST'])
def create_user_endpoint():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    create_user(login, password, is_admin)
    return '', 201



@app.route('/user/<login>', methods=['DELETE'])
def delete_user_endpoint(login):
    delete_user(login)
    return '', 200


if __name__ == '__main__':
    init_db()
    print(get_all_structures())
    app.run(host='0.0.0.0', port=8085)
