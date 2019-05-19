from rest_framework import fields, serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name','description')

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.ReadOnlyField(source='group.name', read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name='photo-detail',format='html')
    class Meta:
        model = Photo
        fields = ('title','flickr_id','description','views','url','group','detail')

class PhotoGetSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='group.name', read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Photo
        fields = ('title','flickr_id','description','views','url','group','tags')


class PhotoGroupSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='owner.username', read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name='photogroup-detail',format='html')
    class Meta:
        model = PhotoGroup
        fields = ('name','description','flickr_id','user','url','detail')

class PhotoGroupGetSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='owner.username', read_only=True)
    photos = PhotoSerializer(many=True,read_only=True)

    class Meta:
        model = PhotoGroup
        fields = ('name','description','flickr_id','user','url','photos')
