from config.celery import app

from .services import evaluate_submission


@app.task
def evaluate_submission_task(submission_id):
    return evaluate_submission(submission_id).pk
