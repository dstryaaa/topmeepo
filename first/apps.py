from django.apps import AppConfig
import secretballot
from django.apps import apps


class FirstConfig(AppConfig):
    name = 'first'

    def ready(self):
        post_model = apps.get_model("first", "Post")
        secretballot.enable_voting_on(post_model, manager_name='votes')
