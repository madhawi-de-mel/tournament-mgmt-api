import logging
from datetime import datetime

from django.contrib.auth.models import Group, User
from django.core.exceptions import MiddlewareNotUsed
from django.core.management import call_command
from django.db import IntegrityError

from management_app.services.match_summary_service import set_won_by
from management_app.services.player_detail_service import set_player_average_score, set_team_average


class StartupMiddleware(object):
    logger = logging.getLogger(__name__)

    def __init__(self, param):
        self.logger.info('Setup started')
        call_command('makemigrations', 'management_app')
        call_command('migrate', 'management_app')
        call_command('migrate')
        try:
            self.create_user_groups()
            self.create_users()
            self.logger.info('Created users and groups')
        except IntegrityError:
            self.logger.info('Users already exists')
        call_command('loaddata', 'tournament.json')
        self.logger.info('Loaded data')
        set_team_average()
        set_player_average_score()
        set_won_by()
        print('Setup complete')
        raise MiddlewareNotUsed('Setup complete')

    @staticmethod
    def create_user_groups():
        group, created = Group.objects.get_or_create(name='admin')
        if created:
            group.name = 'admin'
            group.save()

        group, created = Group.objects.get_or_create(name='coach')
        if created:
            group.name = 'coach'
            group.save()

        group, created = Group.objects.get_or_create(name='player')
        if created:
            group.name = 'player'
            group.save()

    def create_users(self):

        User.objects.create_user('super_user', 'super@gmail.com', 'super123', is_superuser=True, is_staff=True,
                                 last_login=datetime.now())

        admin = User.objects.create_user('admin_a', 'admin.a@gmail.com', 'admin123', last_login=datetime.now(),
                                         is_staff=True)
        self.add_to_group('admin', admin)

        p1 = User.objects.create_user('andrewj', 'tt@tt.com', 'andrewj123', last_login=datetime.now(), is_staff=True)
        self.add_to_group('player', p1)

        c1 = User.objects.create_user('johnd', 'tt@tt.com', 'johnd123', last_login=datetime.now(), is_staff=True)
        self.add_to_group('coach', c1)

    @staticmethod
    def add_to_group(group_name, user):
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        group.save()
