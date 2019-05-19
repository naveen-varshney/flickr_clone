import logging
import requests

from django.shortcuts import render
from django.conf import settings

#third party import
from rest_framework import permissions, viewsets,status
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework.response import Response

#local import
from .serializers import *

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def build_data(request):
    """
     An Authenticated user will pass a valid flickr group id.
     # step-1: get group info by this id and create photo group object
     # step-2: get all the photos related to this group and create photo objects
     **only creating first page objects of photos
    """
    try:
        group_id = request.query_params.get('group_id', '1577604@N20')
        if group_id:
            if PhotoGroup.objects.filter(owner=request.user,flickr_id=group_id).exists():
                return Response({"message":"data already Build for this group id!"}, status=status.HTTP_400_BAD_REQUEST)

            params_list = {
                'method':'flickr.groups.getInfo',
                'api_key':settings.FLICKR_API_KEY,
                'group_id':group_id,
                'format':'json',
                'nojsoncallback':1
            }

            res = requests.get(settings.FLICKR_BASE_URL, params=params_list)
            if res.status_code == 200:
                try:
                    data = res.json().get('group',{})
                except Exception as e:
                     return Response({"message":"Some error occured"}, status=status.HTTP_400_BAD_REQUEST)
                if data.get('stat') != 'ok':
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                group_data = {
                    'flickr_id': data.get('id'),
                    'name': data.get('name',{}).get('_content',''),
                    'description': data.get('description',{}).get('_content'),
                    # 'no_of_photos': data.get('pool_count',{}).get('_content')
                    "url":'http://farm{}.staticflickr.com/{}/buddyicons/{}.jpg'.format(
                            data.get('iconfarm'),
                            data.get('iconserver'),
                            data.get('nsid')
                        )
                }

                #creating group object
                photo_group = PhotoGroup.objects.create(owner=request.user,**group_data)
                logger.info("photo group {} created for flickr_id {}".format(photo_group.id,group_id))

                #for creating photos objects related to this group
                create_group_photos(photo_group,group_id)
                return Response({"message":"group succesfully synced"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error("error occured",exc_info=True)
    return Response({"message":"Some error occured"}, status=status.HTTP_400_BAD_REQUEST)

def create_group_photos(photo_group,group_id):
    try:
        #getting group photos
        params_list = {
            'method':'flickr.groups.pools.getPhotos',
            'api_key':settings.FLICKR_API_KEY,
            'group_id':group_id,
            'format':'json',
            'nojsoncallback':1,
            'per_page':100
        }
        res = requests.get(settings.FLICKR_BASE_URL, params=params_list)
        if res.status_code == 200:
            try:
                data = res.json()
            except Exception as e:
                 logger.error("error occured while getting photos",exc_info=True)
                 return False
            photos = data.get('photos',{}).get('photo',[])
            for photo in photos:
                #to get the description
                photo_detail = get_photo_detail(photo['id'])
                photo_url = 'http://farm{}.staticflickr.com/{}/{}_{}_b.jpg'.format(
                        photo.get('farm'),
                        photo.get('server'),
                        photo.get('id'),
                        photo.get('secret')
                )
                pho = Photo.objects.create(
                    flickr_id = photo['id'],
                    title = photo['title'],
                    description = photo_detail.get('description',{}).get('_content'),
                    url = photo_url,
                    group=photo_group
                )
                #creating tags
                photo_tags = photo_detail.get('tags',{}).get('tags',[])
                for p_tag in photo_tags:
                    tag,created = Tag.objects.get_or_create(name__iexact=p_tag['_content'])
                    if created:
                        pho.tags.add(tag)
                        logger.info('new tag {} created for photo'.format(tag.name))
    except Exception as e:
        logger.error('error ',exc_info=True)

def get_photo_detail(photo_id):
    try:
        params_list = {
            'method':'flickr.photos.getInfo',
            'api_key':settings.FLICKR_API_KEY,
            'photo_id':photo_id,
            'format':'json',
            'nojsoncallback':1
        }
        res = requests.get(settings.FLICKR_BASE_URL, params=params_list)
        return res.json().get('photo',{})
    except Exception as e:
        logger.error("error occured while getting detail for photo_id {}".format(photo_id),exc_info=True)
    return {}

class PhotoViewset(viewsets.ModelViewSet):
    """
    ModelViewSet for photos
    """
    queryset            = Photo.objects.all()
    serializer_class    = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group_id', None)
        if group_id:
            return queryset.filter(group__flickr_id=group_id)
        return queryset
    def get_serializer_class(self):
        if self.action == 'retrieve':
            photo = self.get_object()
            if photo:
                #incresing the views photo have
                photo.views+=1
                photo.save()
            #returning more info in case on single
            return PhotoGetSerializer
        return self.serializer_class # returning default serializers class


class PhotoGroupViewset(viewsets.ModelViewSet):
    """
    ModelViewSet for PhotoGroup
    """
    queryset            = PhotoGroup.objects.all()
    serializer_class    = PhotoGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group_id', None)
        if group_id:
            return queryset.filter(flickr_id=group_id).select_related('photos')
        return queryset
    def get_serializer_class(self):
        if self.action == 'retrieve':
            #returning more info in case on single
            return PhotoGroupGetSerializer
        return self.serializer_class # returning default serializers class
