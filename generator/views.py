from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import Http404
from generator.utils import Generator
from django.views.generic import FormView, ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreatePasswordForm
from .models import Password


class CreatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'generator.html'
    form_class = CreatePasswordForm
    success_url = reverse_lazy('generator')

    def form_valid(self, form):

        length_password = form.cleaned_data['length_password']
        use_uppercase_letters = form.cleaned_data['use_uppercase_letters']
        use_digits = form.cleaned_data['use_digits']
        use_punctuation_characters = form.cleaned_data['use_punctuation_characters']
        custom_characters_allowed = form.cleaned_data['custom_characters_allowed']
        characters_not_allowed = form.cleaned_data['characters_not_allowed']
        password = Generator.generate_password(
            length=length_password,
            use_uppercase=use_uppercase_letters,
            use_numbers=use_digits,
            use_punctuations=use_punctuation_characters,
            customized=custom_characters_allowed,
            not_allowed=characters_not_allowed
        )

        self.request.session['password'] = password
        self.request.session['password_is_new'] = True

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.session.get('password_is_new'):
            context['password'] = self.request.session.get('password')
            self.request.session['password_is_new'] = False
        else:
            if 'password' in self.request.session:
                del self.request.session['password']

        return context


class PasswordListView(LoginRequiredMixin, ListView):

    model = Password
    template_name = 'list-passwords.html'
    context_object_name = 'passwords'
    paginate_by = 5

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user).order_by('id')


class PasswordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Password
    template_name = 'delete_password.html'
    success_url = reverse_lazy('my_passwords')
    http_method_names = ['post']

    def test_func(self):

        password = self.get_object()
        return password.user == self.request.user


class SavePasswordView(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')

        if isinstance(password, str) and password:
            # Calcula métricas
            entropy = Generator.calculate_entropy(password, decimals=2)
            decryption_time = Generator.calculate_decryption_time(entropy, decimals=3)

            # Crea el registro
            Password.objects.create(
                user=request.user,
                password=password,
                entropy=entropy,
                decryption_years_needed=decryption_time
            )

            if 'password' in request.session:
                del request.session['password']

            if 'password_is_new' in request.session:
                del request.session['password_is_new']

        return redirect('my_passwords')
