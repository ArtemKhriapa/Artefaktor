from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text ,Integer, Date # Keyword #
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

#from apps.POI.models import GisPOI
from . import models

connections.create_connection()

class GisPOIIndex(DocType):
    id = Integer()
    date = Date()
    description = Text()
    name = Text()

    class Meta:
        index = 'poi_index'

GisPOIIndex.init()


def bulk_indexing():
    es = Elasticsearch()
    es.indices.delete(index='poi_index', ignore=[400, 404])
    es.indices.create(index='poi_index', ignore=[400])
    GisPOIIndex.init()
    bulk(client=es, actions=(b.indexing() for b in models.GisPOI.objects.all().iterator()))
