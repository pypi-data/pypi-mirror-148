import json
from dapr.clients import DaprClient


def dapr_invoke(app, method, data, http_verb="post", **kwargs):
    """
    dapr http invoke
    
    :param app: app_id
    :param method: 方法名称
    :http_verb: http请求方法
    :return:
    """
    with DaprClient() as d:
        res = d.invoke_method(
            app, method, json.dumps(data), http_verb=http_verb, **kwargs
        )
        return res


def dapr_pubsub(data, pubsub_name="pubsub", topic_name="topic", **kwargs):
    """
    dapr pubsub

    :param pubsub_name: pubsub名称
    :param topic_name: topic名称
    :param data: 数据
    :return:
    """
    with DaprClient() as d:
        res = d.publish_event(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=json.dumps(data),
            data_content_type="application/json",
        )