from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.util.langhelpers import method_is_overridden

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tests:2425@localhost/bycicles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Bycicle(db.Model):
	__tablename__ = 'tbl_bycicles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	model = db.Column(db.String(200))
	price = db.Column(db.Integer)
	brand = db.Column(db.String(200))

	def __init__(self, name, model, price, brand):
		self.name = name
		self.model = model
		self.price = price
		self.brand = brand

db.create_all()

class BycicleSchema(ma.Schema):
	class Meta:
		fields = ( 'id', 'name', 'model', 'price', 'brand' )

bycicle_schema = BycicleSchema()
bycicles_schema = BycicleSchema(many=True)

@app.route('/bycicles', methods=['GET', 'POST'])
def handle_bycicles():
	if request.method == 'POST':
		name = request.json['name']
		model = request.json['model']
		price = request.json['price']
		brand = request.json['brand']
		new_bike = Bycicle(name, model, price, brand)
		db.session.add(new_bike)
		db.session.commit()

		return bycicle_schema.jsonify(new_bike)
	else:
		all_bycicles = Bycicle.query.all()
		result = bycicles_schema.dump(all_bycicles)
		return jsonify(result)

@app.route('/bycicles/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_bycicles_by_id(id):
	if request.method == 'GET':
		bycicle = Bycicle.query.get(id)
		return bycicle_schema.jsonify(bycicle)

	elif request.method == 'PUT':
		bycicle = Bycicle.query.get(id)
		name = request.json['name']
		model = request.json['model']
		price = request.json['price']
		brand = request.json['brand']

		bycicle.name = name
		bycicle.model =model 
		bycicle.price =price 
		bycicle.brand =brand 

		db.session.commit()

		return bycicle_schema.jsonify(bycicle)

	elif request.method == 'DELETE':
		bycicle = Bycicle.query.get(id)
		db.session.delete(bycicle)
		db.session.commit()

		return bycicle_schema.jsonify(bycicle)

if __name__ == '__main__':
	app.run(debug=True)