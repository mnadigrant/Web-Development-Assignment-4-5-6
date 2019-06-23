#!flask/bin/python
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask import url_for
import uuid
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager




auth = HTTPBasicAuth()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mnadi/my-ws/web_dev_assignment4/taskweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate =Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)


class Tasks(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(128))
	title = db.Column(db.String(128))
	description = db.Column(db.String(128))
	done = db.Column(db.Boolean)
	
	def __repr__(self):
		return '<Task {}>'.format(self.title)

@auth.get_password
def get_password(username):
	

	if username=='admin':
		return 'password'
	return None

#users
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
	
	tasks = Tasks.query.all()
	output = []
	
	for task in tasks:
		task_data = {}
		task_data['title'] = task.title
		task_data['public_id'] = task.public_id
		task_data['description'] = task.description
		task_data['done'] = task.done
		output.append(task_data)
	return jsonify({'tasks': output})

@app.route('/todo/api/v1.0/tasks/<public_id>', methods=['GET'])
@auth.login_required
def get_task(public_id):
	
	task = Tasks.query.filter_by(public_id=public_id).first()

	if not task:
		return jsonify({'message':'NO task found'})
	
	task_data = {}
	task_data['title'] = task.title
	task_data['public_id'] = task.public_id
	task_data['description'] = task.description
	task_data['done'] = task.done
		
	return jsonify({'task': task_data})



@app.route('/todo/api/v1.0/createtasks', methods = ['POST'])
@auth.login_required
def create_task():
	data = request.get_json()

	new_task = Tasks(title=data['title'], public_id=str(uuid.uuid4()), description = data['description'], done= False)
	db.session.add(new_task)
	db.session.commit()

	return jsonify({'task': 'new task created'})


@app.route('/todo/api/v1.0/tasks/<public_id>', methods = ['PUT'])
@auth.login_required
def update_task(public_id):
	data = request.get_json()	
	task = Tasks.query.filter_by(public_id=public_id).first()
	
	if not task:
		return jsonify({'message': 'no user found'})
	task.done = True
	
	db.session.commit()
	return jsonify({'message':'THe task data has changed'})
	

@app.route('/todo/api/v1.0/tasks/<public_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(public_id):
	task = Tasks.query.filter_by(public_id=public_id).first()
	
	if not task:
		return jsonify({'message':'No task found'})
	db.session.delete(task)
	db.session.commit()
	
	return jsonify({'message':'Task has been deleted'})


if __name__ == '__main__':
	app.run(host = '0.0.0.0',debug=True, port='5000')

#migrate func
#if __name__ == '__main__':
#	manager.run()
