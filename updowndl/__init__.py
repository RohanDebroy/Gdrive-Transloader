from flask import Flask
from rq import Queue
from worker import conn

app = Flask(__name__)
queue = Queue(connection = conn)

from updowndl import routes
