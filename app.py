from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import start_http_server, Summary, Gauge

# สร้างแอป Flask
app = Flask(__name__)
# กำหนดการเชื่อมต่อฐานข้อมูล MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@mysql:3306/python_api'
# สร้าง SQLAlchemy object เพื่อจัดการฐานข้อมูล
db = SQLAlchemy(app)

# เปิดใช้งาน CORS สำหรับแอปนี้
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Prometheus Metrics
# Summary เพื่อวัดเวลาที่ใช้ในการประมวลผลคำขอ
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# Gauge เพื่อวัดจำนวนรายการในฐานข้อมูล
ITEM_COUNT = Gauge('item_count', 'Number of items in the database')

# สร้าง Model สำหรับตาราง 'Item'
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# สร้าง endpoint สำหรับสร้างรายการใหม่
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(
        name=data['name'],
        price=data['price'],
        currency=data['currency'],
        quantity=data['quantity']
    )
    db.session.add(new_item)
    db.session.commit()
    update_item_count()  # อัปเดตจำนวนรายการในฐานข้อมูล
    return jsonify({'message': 'Item created successfully'}), 201

# สร้าง endpoint สำหรับดึงรายการทั้งหมด
@app.route('/items', methods=['GET'])
@cross_origin()
def get_items():
    items = Item.query.all()
    items_list = [
        {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'currency': item.currency,
            'quantity': item.quantity
        }
        for item in items
    ]
    update_item_count()  # อัปเดตจำนวนรายการในฐานข้อมูล
    return jsonify(items_list), 200

# สร้าง endpoint สำหรับดึง metrics ของ Prometheus
@app.route('/metrics', methods=['GET'])
def metrics():
    from prometheus_client import generate_latest
    return generate_latest(), 200

# ฟังก์ชันสำหรับอัปเดตจำนวนรายการในฐานข้อมูล
def update_item_count():
    count = Item.query.count()
    ITEM_COUNT.set(count)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # สร้างตารางในฐานข้อมูลถ้ายังไม่มี
    start_http_server(8000)  # เริ่มต้น HTTP server สำหรับ Prometheus metrics ที่ port 8000
    app.run(debug=True, host='0.0.0.0', port=5000)  # รันแอป Flask ที่ host '0.0.0.0' และ port 5000
