from django.urls import reverse
from django.shortcuts import redirect
from app.views import is_mfa_setup_invalid, is_finalytics_employee, check_company
def check_mfa_setup_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user
        if user.is_authenticated and is_mfa_setup_invalid(user) and request.path.startswith('/admin'):
            return redirect('two_factor:setup')
        elif user.is_authenticated:
            co, ugs, context = check_company(request, {})
            if context['is_fin_employee'] and (request.path.startswith('/admin/app/adtemplate/') or request.path.startswith('/admin/app/adcopy/') or request.path.startswith('/admin/app/offer/') or request.path.startswith('/admin/app/faqquestion/') or request.path.startswith('/admin/auth/user/') or request.path.startswith('/admin/app/keywordgroup/')):
            # del request.session['cu_id']
                if 'cu_id' not in request.session and 'cu_id' not in request.GET:
                    # request.session['cu_id'] = 'all'
                    request.session['redirect_url'] = request.path
                    return redirect(reverse('choose-company'))            

        
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware