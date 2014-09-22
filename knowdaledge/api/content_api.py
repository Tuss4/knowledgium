from rest_framework import status, views, generics
from rest_framework.response import Response


from content import serializers as srlzr
from content.permissions import ContentPermission, CategoryPermission
from content.models import Content, Category


class ContentListCreateView(generics.ListCreateAPIView):

    serializer_class = srlzr.ContentSerializer
    permission_classes = (ContentPermission,)
    queryset = Content.objects.all()

    def post(self, request):
        serializer = srlzr.CreateContentSerializer(data=request.DATA)
        if serializer.is_valid():
            content = Content.objects.create(
                author_id=self.request.user.pk,
                title=serializer.data.get('title'),
                message=serializer.data.get('message'),
                category_id=serializer.data.get('category'))
            result = srlzr.CreateContentResponseSerializer()
            result.data['url'] = content.get_absolute_url()

            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = srlzr.ContentSerializer
    permission_classes = (ContentPermission,)
    queryset = Content.objects.all()


class CategoryListCreateView(generics.ListCreateAPIView):

    permission_classes = (CategoryPermission,)
    serializer_class = srlzr.CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = (CategoryPermission,)
    serializer_class = srlzr.CategorySerializer
    queryset = Category.objects.all()
