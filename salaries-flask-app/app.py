from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

e = create_engine('sqlite:///salaries.db')
app = Flask(__name__)
api = Api(app)

class Dept_Meta(Resource):
	def get(self):
		conn = e.connect()
		query = conn.execute("select distinct DEPARTMENT from salaries")
		return {'departments': [i[0] for i in query.cursor.fetchall()]}

class Dept_Salary(Resource):
	def get(self, department_name):
		conn = e.connect()
		query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
		result = {'data': [dict(zip(tuple (query.keys()),i)) for i in query.cursor]}
		return result

api.add_resource(Dept_Salary,'/dept/<string:department_name>')
api.add_resource(Dept_Meta,'/departments')

if __name__ == '__main__':
	app.run()
