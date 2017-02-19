# TODO, explore get_delete_url
# TODO, change order
# TODO, explore decimal rounding on money

"""
TODO, when i delete all migrations except the migration folder and __init__.py file it will not let me migrate
because of the service_group form. I need to comment out my forms and put this in its place to get makemigrations to
run

class StandardConcreteForm:
    pass


class DecorativeConcreteForm:
    pass


class StepsForm:
    pass


class FoundationForm:
    pass


class FootingsForm:
    pass


class EgressWindowForm:
    pass

after nuking db:
python populate_services_db.py
python manage.py createsuperuser
"""
