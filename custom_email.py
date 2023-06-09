from django.urls import reverse
from djoser.email import ActivationEmail

from djoser.email import ConfirmationEmail


class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()

        # Extract uid and token from the activation URL
        activation_url = self.user_url
        uid = activation_url.split('?uid=')[1].split('&token=')[0]
        token = activation_url.split('&token=')[1]

        # Build the activation URL without query parameters
        activation_url = activation_url.split('?')[0]

        # Update the context with uid and token
        context['uid'] = uid
        context['token'] = token
        context['activation_url'] = activation_url

        return context


class CustomConfirmationEmail(ConfirmationEmail):
    template_name = "email/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['activation_status'] = "activated"
        return context
