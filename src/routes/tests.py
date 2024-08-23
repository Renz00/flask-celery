import json
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, make_response
from celery.result import AsyncResult
from typing import Dict, List

from .. import db, app
from ..models import User, Post
from ..celery.tasks import get_user_posts

tests = Blueprint('tests', __name__)


@tests.route('/posts/<int:user_id>', methods=['GET'])
def posts(user_id: int):
    task = get_user_posts.delay(user_id)
    return make_response({'task_id': task.id, 'success': True}), 200
    
    
@tests.route('/result/<string:task_id>', methods=['GET'])
def result(task_id: str):
    result = AsyncResult(task_id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
        "result": result.get()
    }
    

@tests.route('/status/<string:task_id>', methods=['GET'])
def status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "status": result.status,
        "state": result.state,
        "successful": result.successful(),
        "result": result.result,
    }