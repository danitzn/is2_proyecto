from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        # Authenticate the user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return '/admin'