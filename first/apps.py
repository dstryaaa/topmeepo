from django.apps import AppConfig
import first
import secretballot


class FirstConfig(AppConfig):
    name = 'first'

    def ready(self):
        Post = first.get_model("first", "Post")
        secretballot.enable_voting_on(Post)
