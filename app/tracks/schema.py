import graphene
from graphene_django import DjangoObjectType
from .models import Track, Like
from users.schema import UserType
from graphql import GraphQLError

class TrackType(DjangoObjectType):
    """Class that contains all the Tracks called by graphene"""
    class Meta:
        """Adding meta class that overides the Track model"""
        model = Track

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
class Query(graphene.ObjectType):
    """Class of query Type to list all tracks"""
    tracks = graphene.List(TrackType)
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info):
        """ Returns list of track objects"""
        return Track.objects.all()

    def resolve_likes(self, info):
        """ Returns list of like objects"""
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user or None
        
        if user.is_anonymous:
            raise GraphQLError('Log in first to add track.')

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
            raise GraphQLError('Not permitted to update this track')

        track.title = title
        track.description = description
        track.url = url

        track.save()
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError('Not permitted to delete this track')

        track.delete()
        return DeleteTrack(track_id=track_id)

class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
     class Arguments:
            track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

         if user.is_anonymous:
             raise GraphQLError('Log in first to like the track.')

        track = Track.objects.get(id=track_id)

        if not track:
            raise GraphQLError('there no traack for the provided track')
        
        Like.objects.create(
            user=user,
            track=track
        )

        return CreateLike(user=user, track=track)
class Mutation(graphene.ObjectType):
      created_track = CreateTrack.Field()
      update_track = UpdateTrack.Field()
      delete_track = DeleteTrack.Field()
      create_like = CreateLike.Field()