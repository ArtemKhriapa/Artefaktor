from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from apps.POI.api.serializers  import  GisPOISerializer, ListGisPOISerializer
from apps.POI.api.serializers  import NewDraftGisPOISerializer, CategorySerializer #,ListESSerializer
from apps.POI.models import GisPOI as GisPOI_model
from apps.POI.models import DraftGisPOI as DraftGisPOI_model
from apps.POI.models import Category as Category_model
from rest_framework_gis.filters import InBBoxFilter
from apps.filter.models import PointInRadiusFilter, CategoryFilter
from elasticsearch import Elasticsearch, RequestsHttpConnection
from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from apps.POI.esearch import GisPOIIndex
from rest_framework.response import Response


class CustomPagePagination(PageNumberPagination):
    #class for set pagination parameters
    page_size = 10 #obj in page
    page_size_query_param = 'page_size'
    max_page_size = 10


class NewDraftGisPOIView(generics.CreateAPIView):
    queryset = DraftGisPOI_model.objects.all()
    serializer_class = NewDraftGisPOISerializer

    def post(self, *args, **kwargs):
            res = super().post(*args, **kwargs)
            res.status_code == status.HTTP_201_CREATED
            return res


class ListGisPOIView(generics.ListAPIView):
    queryset = GisPOI_model.objects.all().order_by('id') # sorted by id ?
    serializer_class = ListGisPOISerializer
    pagination_class = CustomPagePagination
    bbox_filter_field = 'point'
    distance_filter_field = 'point'
    distance_filter_convert_meters = True
    bbox_filter_include_overlapping = True
    distanc_filter_include_overlapping = True
    filter_backends =(DjangoFilterBackend, filters.SearchFilter, InBBoxFilter, PointInRadiusFilter,CategoryFilter)#
    filter_fields = ('name','description') # filter with 100% match in fields ?
    search_fields = ('name','description', 'addres') #search partial match in all of this fields ?

    # def get_queryset(self, *args, **kwargs):
    #     return GisPOI_model.objects.all()


class GisPOIView(generics.RetrieveAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = GisPOISerializer

    def get_object(self):
        return get_object_or_404(GisPOI_model, id=self.kwargs.get('POI_id'))


class ListCategoryView(generics.ListAPIView):
    queryset = Category_model.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = CustomPagePagination
    search_fields = ('name','id') # why filter breaks down if one field ??


class GisPOIESView(es_views.ListElasticAPIView):
    # print('in view')
    serializer_class = ListGisPOISerializer
    es_client = Elasticsearch(hosts=['http://localhost:9200/'],connection_class=RequestsHttpConnection)
    es_model = GisPOIIndex
    es_filter_backends = (es_filters.ElasticFieldsFilter, es_filters.ElasticSearchFilter)
    es_search_fields = ('name','description',)


    def do_search(self):
        search =super().do_search()
        objs = GisPOI_model.objects.filter(pk__in=[i.id for i in search])
        # print(objs,"!YES, it's POIs!!!!!!!!!!!!!!!!!") #
        return  search #, objs

    def get_queryset(self, *args, **kwargs):
        # print('in get QS')
        indxs = super().get_queryset()
        # print('--------------->',indxs)
        objs = GisPOI_model.objects.filter(pk__in=[i['id'] for i in indxs])
        # print('heere -----------', objs)
        return objs

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # paginator = CustomPagePagination()
        # result_page = paginator.paginate_queryset(queryset, request)
        # serializer = GisPOISerializer(result_page, many = True)
        # res = paginator.get_paginated_response(serializer.data)
        serializer = [GisPOISerializer(i) for i in queryset]
        data = [i.data for i in serializer]
        # print(data)

        return Response(data) #super().get(self, request, *args, **kwargs) # data
