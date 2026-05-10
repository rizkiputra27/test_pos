from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Konfigurasi Database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'counter_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# =========================
# Ambil semua data
# =========================
@app.route('/transaksi', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transaksi_tf ORDER BY id DESC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

# =========================
# Tambah data
# =========================
@app.route('/transaksi', methods=['POST'])
def add_data():
    new_data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO transaksi_tf 
    (no_urut, tanggal, penyetor, bank, nominal, fee_admin, total, margin) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        new_data['No'],
        new_data['Tanggal'],
        new_data['No HP'],
        new_data['Bank'],
        new_data['Nominal'],
        new_data['Fee Admin'],
        new_data['Total'],
        new_data['Margin']
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Data berhasil disimpan"
    }), 201

# =========================
# Hapus semua data
# =========================
@app.route('/transaksi/hapus-semua', methods=['DELETE'])
def delete_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE transaksi_tf")
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Semua data berhasil dihapus"
    })

# =========================
# Jalankan server
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)