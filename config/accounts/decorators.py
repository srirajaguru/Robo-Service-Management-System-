from django.contrib.auth.decorators import user_passes_test


def is_internal_user(user):
    return user.is_authenticated and (user.is_superuser or hasattr(user, "staffprofile"))


def staff_required(view):
    return user_passes_test(is_internal_user, login_url="login")(view)


def admin_required(view):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_superuser,
        login_url="login",
    )(view)
