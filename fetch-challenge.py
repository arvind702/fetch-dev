import datetime
import json
import math
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)
db = {}

def score_receipt(receipt_json):
    alnum_score = sum(x.isalnum() for x in receipt_json['retailer'])
    float_score = 50 * (float(int(float(receipt_json['total']))) == float(receipt_json['total'])) 
    quarter_score = 25 * ((float(receipt_json['total']) * 100) % 25 == 0)
    pairs_score = 5 * (len(receipt_json['items']) // 2)
    length_score = sum([math.ceil(float(i['price']) * 0.2) if len(i['shortDescription'].strip()) % 3 == 0 else 0 for i in receipt_json['items']])
    date_score = 6 * (datetime.datetime.strptime(receipt_json['purchaseDate'], '%Y-%m-%d').day % 2 != 0)
    time_score = 10 * (lambda h, m: (h == '14' or h == '15') and not (h == '14' and m == '00'))(*receipt_json['purchaseTime'].split(':'))

    return sum([v if k.endswith('score') else 0 for k, v in vars().items()])

def store_score(score):
    r_id = str(uuid.uuid4())
    db[r_id] = score

    return r_id

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            r_id = store_score(score_receipt(request.json))
            return jsonify({'id': r_id})
        except:
            pass

    return jsonify({'error': 'bad request'}), 400

@app.route('/receipts/<r_id>/points', methods=['GET'])
def get_score(r_id):
    if r_id in db:
        return jsonify({'points': db[r_id]})

    return jsonify({'error': 'not found'}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
