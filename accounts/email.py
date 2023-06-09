from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings
from django.urls import reverse


class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)

        activation_url = reverse(
            "useraccount-activation")  # Replace "activation-url" with your actual activation URL endpoint name
        activation_url = f"{activation_url}?uid={uid}&token={token}"

        context["uid"] = uid
        context["token"] = token
        context["url"] = activation_url
        return context

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()

        # Generate the token
        token = default_token_generator.make_token(self.user)

        # Build the activation URL with uid and token as parameters
        uid = str(self.user.id)
        activation_url = reverse('useraccount-activation')
        activation_url += f'?uid={uid}&token={token}'

        # Update the context with activation URL
        context['activation_url'] = activation_url
        print(activation_url)

        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"


class CustomConfirmationEmail(ConfirmationEmail):
    template_name = "email/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['activation_status'] = "activated"
        return context


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
