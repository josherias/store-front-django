from re import M
from typing import Collection
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from store.pagination import DefaultPagination
from .models import Cart, OrderItem, Product, Collection, Review
from .serializers import CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id']
    pagination_class = DefaultPagination
        
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count > 0:
            return Response({ 'error':"Product belongs to an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super.destroy(request, *args, **kwargs)
              
        # delete method changes to destroy to prevent showing it on the product list
  
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all() 
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error': 'Collection cannot be deleted'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super.destroy(request, *args, **kwargs)
            


class ReviewViewSet(ModelViewSet):
        # queryset = Review.objects.all()
        serializer_class = ReviewSerializer
        
        # usd method coz we dint have access to the self 
        def get_queryset(self):
             return Review.objects.filter(product_id=self.kwargs['product_pk'])
        
        # context passes data to serializer
        def get_serializer_context(self):
             return {'product_id': self.kwargs['product_pk']}
        

class CartViewSet(CreateModelMixin, GenericViewSet): #only require a few methods allowed here
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
      

 
       




# API VIEW IS THE BASE CLASS FOR ALL CLASS BASED VIEWS
# MIXIN CLLASS THAT INCAPSULATES PATTERN OF CODE

# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({ 'error':"Product belongs to an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# GENERIC VIEWS COMBINE THE MIXIN LOGIN AND THEY ARE OFTENLY USED


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     # OVERIDE THE DEFAULT GET QUERYSET METHOD and geting serializer
#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()
#         # replaces this [queryset = Product.objects.select_related('collection').all()]
    
#     def get_serializer(self):
#         return ProductSerializer
#         # replaces this [ProductSerializer(queryset, many=True, context={'request': request})]
        
#     def get_serializer_context(self):
#         return {'request': self.request}
#         # replaces this [context={'request': request}]


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        

# SITUATUONS GENERIC VIEW MAY NOT WORK AND WE CUSTOMIZE
# DEFAULT IMPLEMENTATION
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({ 'error':"Product belongs to an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# VIEWSESTS COMBINE LOGIC FOR MULTIPLE CREATE VIEWS IN AS INGLE CLASS
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
        
#     def get_serializer_context(self):
#         return {'request': self.request}
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # logic from retrieve and put alreday in mixin but fr delete it changes



# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all() 
#     serializer_class = CollectionSerializer
     
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(
#         products_count=Count('products')),pk=pk)
        
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted'}, 
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)