from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    number_rating = serializers.IntegerField(read_only=True)
    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    # def get_len_name(self,object):
    #     return len(object.name)
   
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description should be differnet!")
    #     else:
    #         return data
    
    # def validate_name(self,value):
        
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is Too short!")
    #     else:
    #         return value
        
        
# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short!")
#     else:
#         return value

# class WatchlistSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators = [name_length] )
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Watchlist.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description should be differnet!")
#         else:
#             return data
    
#     # def validate_name(self,value):
        
#     #     if len(value)<2:
#     #         raise serializers.ValidationError("Name is Too short!")
#     #     else:
#     #         return value