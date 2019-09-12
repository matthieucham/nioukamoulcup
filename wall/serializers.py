from django.apps import apps
from rest_framework import serializers
from wall.models import Post


class PostSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    author = serializers.SlugRelatedField('username', read_only=True)

    def get_replies(self, obj):
        reps = list()
        for rep in obj.replies.order_by('created_at').all():
            reps.append(PostSerializer(context=self.context).to_representation(rep))
        return reps

    class Meta:
        model = Post
        fields = '__all__'

