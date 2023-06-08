from django.conf import settings

def env(request):
    # return any necessary values
    return {
        'PIXEL_SCRIPT_URL': settings.PIXEL_SCRIPT_URL,
        'EXTERNAL_SITE_IP': settings.EXTERNAL_SITE_IP,
    }