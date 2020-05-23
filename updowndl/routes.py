from updowndl import app, queue, conn
from flask import request, jsonify
from rq.job import Job
from .downloader import upDown
import shutil
import glob
import json

@app.route('/')
@app.route('/index')
def index():
    return 'I am working fine'


@app.route('/api', methods=['GET', 'POST'])
def transload():
    if request.method == "POST":
        url = request.form['url']
    else:
        url = request.args.get('url')

    job = queue.enqueue(upDown, args=(url,), timeout=86400, result_ttl=86400)

    return jsonify(job_id=job.get_id())


@app.route('/api/result', methods=['GET', 'POST'])
def result():
    if request.method == "POST":
        job_id = request.form['job_id']
    else:
        job_id = request.args.get('job_id')

    job = Job.fetch(job_id, connection=conn)

    if job.is_finished:
        description = job.description.replace(
            "updowndl.downloader.upDown('", '').replace("')", '')
        return jsonify(job_id=job_id, description=description, downloadUrl=job.return_value, status='Finished'), 200
    elif job.is_queued:
        return jsonify(job_id=None, description=None, downloadUrl=None, status='Queued')
    elif job.is_started:
        return jsonify(job_id=None, description=None, downloadUrl=None, status='Processing')
    elif job.is_failed:
        return jsonify(job_id=None, description=None, downloadUrl=None, status='Failed')


@app.route("/admin/<p>", methods=['GET'])
def admin(p):
    if p == 'clean':
        shutil.rmtree("data/")
        return 'Done'
    elif p =='list':
        x = glob.glob("data/*")
        print(x)
        return jsonify(files=tuple(x))
