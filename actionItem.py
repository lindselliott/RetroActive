import json 

class ActionItem:
	def __init__(self, owner, assigned_to, start_date, end_date, task, completed):
		self.owner = owner
		self.assigned_to = assigned_to
		self.start_date = start_date
		self.end_date = end_date
		self.task = task
		self.completed = completed

	@property
	def owner(self):
		return self.owner

	@property
	def assigned_to(self):
		return self.assigned_to

	@property
	def start_date(self):
		return self.start_date

	@property
	def end_date(self):
		return self.end_date

	@property
	def task(self):
		return self.task

	@property
	def completed(self):
		return self.completed

	def serialize(self):
		return {
			'owner': self.owner, 
			'assigned_to': self.assigned_to,
			'start_date': self.start_date,
			'end_date': self.end_date,
			'task': self.task,
			'completed': self.completed
		}

