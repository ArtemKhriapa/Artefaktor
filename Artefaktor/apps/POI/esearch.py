from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text ,Integer, Date # Keyword #
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

#from apps.POI.models import GisPOI
from . import models

connections.create_connection()

class GisPOIIndex(DocType):
    #author = Text()
    #date = Date()
    #id = Integer()
    description = Text()
    name = Text()
   # tags = Keyword(multi=True)

    class Meta:
        index = 'gis-index'

GisPOIIndex.init()


def bulk_indexing():
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.GisPOI.objects.all().iterator()))