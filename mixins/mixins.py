from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


class OwnerMixin(object):
    def get_object(self, queryset=None):
        """Returns the object the view is displaying."""

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(pk=pk, user=self.request.user, )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied

        return obj


# class PaginateDataMixin(object):
#     def get_context_data(self):
#
#
#
#         return context