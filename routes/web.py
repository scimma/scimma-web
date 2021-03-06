import json

from flask import abort, Blueprint, redirect, render_template, request, url_for
from scimma.client import stream

from client import ScimmaClientWrapper
# from extensions import db
from forms import CreateTopicForm, PublishForm
from models import Message, Topic


KAFKA_HOST = 'localhost'
# KAFKA_HOST = 'firkraag.lco.gtn'
KAFKA_PORT = '9092'

kafka_config = {
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'group.id': 'scimma-web-test',
    'auto.offset.reset': 'earliest'
}

client_wrapper = ScimmaClientWrapper(**kafka_config)

web_bp = Blueprint('', 'web')


@web_bp.route('/', methods=['GET'])
def home():
    """
    Presents a brief intro and site map.
    """
    return render_template('home.html')


@web_bp.route('/topic/list', methods=['GET'])
def list_topics():
    """
    Returns the list of topics and number of messages per topic
    """
    context = {
        'results': Topic.query.all()
    }
    return render_template('topic_index.html', context=context)


@web_bp.route('/topic/create', methods=['GET', 'POST'])
def create_topic():
    form = CreateTopicForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            t = Topic(name=form.topic_name.data)
            t.save()
            return redirect(url_for('.list_topics'))
        except Exception as e:
            abort(500)
    return render_template('topic_create.html', form=form)

@web_bp.route('/topic/<int:topic_id>', methods=['GET'])
def get_topic(topic_id):
    """
    Returns from the database the messages for a specific topic
    """

    context = {
        'results': [message for message in Message.query.filter_by(topic_id=topic_id).all()]
    }
    return render_template('message_index.html', context=context)


@web_bp.route('/message/', methods=['GET'])
def list_messages():
    """
    Returns a list of all messages
    """
    context = {
        'results': Message.query.all()
    }
    return render_template('message_index.html', context=context)


@web_bp.route('/message/create', methods=['GET', 'POST'])
def publish_message():
    """
    Allows a user to publish an alert to the given topic
    The published alert goes to the Kafka stream, then ingested into the db.
    """
    form = PublishForm(request.form)
    form.topic.choices = [(topic.name, topic.name) for topic in Topic.query.all()]
    message = {
        'title': form.title.data,
        'number': form.number.data,
        'subject': form.subject.data,
        'publisher': form.publisher.data,
        'content': form.content.data
    }
    if request.method == 'POST' and form.validate():
        with stream.open(f'kafka://{KAFKA_HOST}:{KAFKA_PORT}/{form.topic.data}', 'w', format='json') as s:
            s.write(message)
        return redirect(url_for('.list_messages'))
    return render_template('publish_form.html', form=form)


@web_bp.route('/message/<int:msg_id>', methods=['GET'])
def get_message(msg_id):
    """
    Displays the content of a specific message
    """
    context = {
        'message': Message.query.get(msg_id)
    }

    return render_template('message_detail.html', context=context)
