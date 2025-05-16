from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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

        user = self.request.user
        length_password = form.cleaned_data['length_password']
        use_uppercase_letters = form.cleaned_data['use_uppercase_letters']
        use_digits = form.cleaned_data['use_digits']
        use_punctuation_characters = form.cleaned_data['use_punctuation_characters']
        customized = form.cleaned_data['customized']
        not_allowed = form.cleaned_data['not_allowed']

        password = Generator.generate_password(
            length=length_password,
            use_uppercase=use_uppercase_letters,
            use_numbers=use_digits,
            use_punctuations=use_punctuation_characters,
            customized=customized,
            not_allowed=not_allowed

        )

        entropy = Generator.calculate_entropy(
            password=password,
            decimals=2
        )

        decryption_years_needed = Generator.calculate_decryption_time(
            entropy=entropy,
            decimals=3
        )

        Password.objects.create(
            user=user,
            password=password,
            entropy=entropy,
            decryption_years_needed=decryption_years_needed
        )

        self.request.session['password'] = password

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        password = self.request.session.pop('password', None)
        context['password'] = password

        return context


class PasswordListView(LoginRequiredMixin, ListView):

    model = Password
    template_name = 'list-passwords.html'
    context_object_name = 'passwords'
    paginate_by = 3

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user).order_by('id')


class PasswordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Password
    template_name = 'delete_password.html'
    success_url = reverse_lazy('my_passwords')

    def test_func(self):

        password = self.get_object()
        return password.user == self.request.user
