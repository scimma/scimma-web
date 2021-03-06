from flask import abort, Blueprint

from models import Message, Topic


api_bp = Blueprint('/v1', 'api_v1')


@api_bp.route('/v1/message',  methods=['GET'])
def message_list():
    return {'messages': [message.serialize() for message in Message.query.all()]}


@api_bp.route('/v1/message', methods=['POST'])
def message_create():
    abort(501)


@api_bp.route('/v1/message/<int:msg_id>', methods=['GET'])
def message_get(msg_id):
    return Message.query.get(msg_id).serialize()


@api_bp.route('/v1/message/<int:msg_id>', methods=['POST'])
def message_update(msg_id):
    abort(501)


@api_bp.route('/v1/message/<int:msg_id>', methods=['DELETE'])
def message_delete(msg_id):
    abort(501)


@api_bp.route('/v1/topic',  methods=['GET'])
def topic_list():
    return {'topics': [topic.serialize() for topic in Topic.query.all()]}


@api_bp.route('/v1/topic', methods=['POST'])
def topic_create():
    abort(501)


@api_bp.route('/v1/topic/<int:topic_id>', methods=['GET'])
def topic_get(topic_id):
    return Topic.query.get(topic_id).serialize()


@api_bp.route('/v1/topic/<int:topic_id>', methods=['POST'])
def topic_update(topic_id):
    abort(501)


@api_bp.route('/v1/topic/<int:topic_id>', methods=['DELETE'])
def topic_delete(topic_id):
    abort(501)
