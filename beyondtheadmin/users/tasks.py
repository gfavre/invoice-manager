from django.contrib.auth import get_user_model

from config import celery_app


User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def create_stripe_customer(user_id):
    user = User.objects.get(id=user_id)
    user.create_stripe_customer()
