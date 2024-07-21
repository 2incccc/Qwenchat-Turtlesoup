from dashscope import Application
from http import HTTPStatus

def get_answer(question, session_id=None):
    response = Application.call(
        app_id='cbe1fe12afb0498386debffa5b97d64b',
        prompt=question,
        session_id=session_id,
        api_key='sk-BNLGIuMgi7'
    )
    return response

def init_session():
    response = Application.call(
        app_id='cbe1fe12afb0498386debffa5b97d64b',
        prompt='开始游戏',
        api_key='sk-BNLGIuMgi7'
    )
    return response
