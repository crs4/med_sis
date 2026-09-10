from django.http import Http404
from django.urls import resolve

class RestrictProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply restrictions to authenticated, non-staff users
        if request.user.is_authenticated and not request.user.is_staff:
            current_url = resolve(request.path_info)
            
            # GeoNode's profile detail view namespace is typically 'profile_detail'
            if current_url.url_name == 'profile_detail':
                url_username = current_url.kwargs.get('username')
                
                # If they are trying to access someone else's profile, throw a 404
                if url_username and request.user.username != url_username:
                    raise Http404("Profile not found or is private.")

        return self.get_response(request)