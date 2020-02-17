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

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()
        

    def mutate(self, info, title, description, url):
        track = Track(title=title, description=description, url=url)
        track.save()
        return CreateTrack(track=track)

class Mutation(graphene.ObjectType):
      created_track = CreateTrack.Field()