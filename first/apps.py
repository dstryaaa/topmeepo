from django.apps import AppConfig
import first
import secretballot


class FirstConfig(AppConfig):
    name = 'first'

    def ready(self):
        post_model = first.get_model("first", "Post")
        secretballot.enable_voting_on(post_model)
