from celery import shared_task

from zoo.elasticsearch.indexer import Indexer


@shared_task
def index_model_instances():
    indexer = Indexer()
    indexer.index_specified_models()


def index_openapi_definitions():
    indexer = Indexer()
    indexer.index_specified_models()
