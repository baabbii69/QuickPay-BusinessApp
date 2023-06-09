from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _


class ActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        user = context.get('user')
        uid = utils.encode_uid(user.pk)
        token = self.token
        activation_url = reverse('useraccount-activation')
        activation_url = f"{activation_url}?uid={uid}&token={token}"
        context['url'] = activation_url
        return context

    def get_activate_url(self, context):
        current_site = get_current_site(self.request)
        return self.request.build_absolute_uri(
            f"{settings.DJOSER.get('ACTIVATION_URL')}/{context['uid']}/{context['token']}"
        )

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        user = context.get('user')
        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        activation_url = reverse('useraccount-activation')
        activation_url = f"{activation_url}?uid={uid}&token={token}"
        context['activate_url'] = self.request.build_absolute_uri(activation_url)
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/username_changed_confirmation.html"


class UsernameResetEmail(BaseEmailMessage):
    template_name = "email/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
        return context
