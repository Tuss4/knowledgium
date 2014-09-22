from rest_framework import serializers


from .models import Content, Category
from coder.serializers import CoderSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')


class ContentSerializer(serializers.ModelSerializer):

    author = CoderSerializer()
    category = CategorySerializer()

    class Meta:
        model = Content
        fields = ('id', 'author', 'title', 'message', 'created', 'updated', 'category')


class CreateContentSerializer(serializers.Serializer):

    title = serializers.CharField()
    message = serializers.CharField()
    category = serializers.IntegerField(required=False)


class CreateContentResponseSerializer(serializers.Serializer):

    url = serializers.URLField()
