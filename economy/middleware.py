import tldextract

from users.models import Profile
from users import views as user_views


class URLChangeMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        ext = tldextract.extract(request.build_absolute_uri())
        try:
            profile = Profile.objects.get(subdomain=ext.subdomain)
        except Profile.DoesNotExist:
            profile = None
        response = self._get_response(request)
        if ext.subdomain and request.get_full_path() == '/':
            kwargs = {}
            if request.user.profile != profile:
                kwargs = {'user': profile.id}
            response = user_views.profile(request, kwargs)
        return response
