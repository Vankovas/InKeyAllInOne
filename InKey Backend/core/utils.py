def is_user_auth(request):
    return request and hasattr(request, "user") and request.user.is_authenticated
