class CurrentCoderMixin(object):

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()
