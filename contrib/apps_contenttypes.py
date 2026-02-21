from django.contrib.contenttypes.apps import ContentTypesConfig


class MongoContentTypesConfig(ContentTypesConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
