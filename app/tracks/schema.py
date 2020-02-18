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
        user = info.context.user or None
        
        if user.is_anonymous:
            raise Exception('Log in first to add track.')

        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String() 

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user

        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception('Not permitted to update this track')

        track.title = title
        track.description = description
        track.url = url

        track.save()
        return UpdateTrack(track=track)


class Mutation(graphene.ObjectType):
      created_track = CreateTrack.Field()
      update_track = UpdateTrack.Field()