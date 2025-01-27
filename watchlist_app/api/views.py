from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
        
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already review this movie!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)
    
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        Review.objects.filter(watchlist = pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ViewSet):
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)



class StreamPlatformAV(APIView):
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        seriializer = StreamPlatformSerializer(data = request.data)
        if seriializer.is_valid():
            seriializer.save()
            return Response(seriializer.data)
        else:
            return Response(seriializer.errors)
        
class StreamDetailAV(APIView):
    
    def get(self, request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response({'Error: Id Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        data = StreamPlatform.objects.get(pk=pk)
        seriializer = StreamPlatformSerializer(data, request.data)
        if seriializer.is_valid():
            seriializer.save()
            return Response(seriializer.data)
        else:
            return Response(seriializer.errors)
        
class WatchListAV(APIView):
    
    def get(self, request):
        Watchlists = WatchList.objects.all()
        serializer = WatchListSerializer(Watchlists, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchlistDetailAV(APIView):
    def get(self,request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)     
        except WatchList.DoesNotExist:
            return Response({'error':'WatchList not found'}, status=status.HTTP_404_NOT_FOUND) 
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(sef,request,pk):
        watchlist = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchlist,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        watchlist = WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
# @api_view(['GET','POST'])
# def Watchlist_list(request):
#     if request.method == 'GET':
#         Watchlists =  WatchList.objects.all()
#         serializer = WatchlistSerializer(Watchlists,many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = WatchlistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        

# @api_view(['GET','PUT','DELETE','PATCH'])
# def Watchlist_details(request,pk):
#     if request.method == 'GET':
#         try:
#             WatchList = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'Error':'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
      
#         serializer = WatchlistSerializer(WatchList)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         data = WatchList.objects.get(pk=pk)
#         serializer = WatchlistSerializer(data,request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'PATCH':
#         data = WatchList.objects.get(pk=pk)
#         serializer = WatchlistSerializer(data, request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'DELETE':
#         data = WatchList.objects.filter(pk=pk).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        