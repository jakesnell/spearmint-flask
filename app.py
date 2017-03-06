import pprint
import json
from time import localtime, strftime
from flask import Flask, render_template, request

from spearmint.utils.database.mongodb import MongoDB

app = Flask(__name__)

db = MongoDB(database_address='localhost')

def format_value(v):
    return "{:0.4f}".format(v)

def format_date(t):
    return strftime("%m/%d/%y %I:%M %p", localtime(t))

def format_params(params):
    ret = { }
    for k,v in params.iteritems():
        assert v['values'].ndim == 1
        assert v['values'].shape[0] == 1
        ret[k] = float(format_value(v['values'][0]))
    return ret

def format_job(job):
    print job
    return {
        'id': job['id'],
        'value': format_value(job['values']['main']) if 'values' in job else '',
        'status': job['status'],
        'end_time': format_date(job['end time']),
        'end_time_value': job['end time'],
	'params': format_params(job['params'])
    }

@app.route("/")
def home():
    experiment_name = request.args.get('id')
    experiment = {
        'name': experiment_name,
        'language': 'python',
        'params': [{
            'name': 'temp'
        }]
    }
    jobs = db.load(experiment_name, 'jobs')
    return render_template(
        'home-bootstrap.html',
        experiment=experiment,
        jobs=map(format_job, jobs)
    )

@app.route("/status")
def status():
    experiment_name = request.args.get('id')
    jobs = db.load(experiment_name, 'jobs')
    return render_template('status.html', jobs=jobs)

if __name__ == "__main__":
    app.run()
