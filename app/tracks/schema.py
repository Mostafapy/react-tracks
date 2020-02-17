import graphene
from graphene_django import DjangoObjectType
from .models import Track

class TrackType(DjangoObjectType):
    """Class that contains all the Tracks called by graphene"""
    class Meta:
        """Adding meta class that overides the Track model"""
        model = Track

class Query(graphene.ObjectType):
    """Class of query Type to list all tracks"""
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        """ Returns list of track objects"""
        return Track.objects.all()
    