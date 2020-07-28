import logging

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MiddlewareNotUsed
from django.core.management import call_command
from django.db import IntegrityError
from django.utils import timezone

from management_app.constants.group_permission import GroupPermission
from management_app.constants.user_group import UserGroup
from management_app.models import UserProfile, Coach, Player
from management_app.utils.tournament_detail_util import set_player_average_score, set_team_average, set_won_by


class StartupMiddleware(object):
    logger = logging.getLogger(__name__)

    def __init__(self, param):
        self.logger.info('Startup: Setup started')
        call_command('makemigrations', 'management_app')
        call_command('migrate', 'management_app')
        call_command('migrate')
        # load data
        call_command('loaddata', 'tournament.json')

        # create users and groups
        try:
            self.create_user_groups()
            self.create_users()
            self.logger.info('Startup: Created users and groups')
        except IntegrityError:
            self.logger.info('Startup: Users already exist')

        self.logger.info('Startup: Loaded data')
        set_team_average()
        set_player_average_score()
        set_won_by()
        print('Startup: Setup complete')
        raise MiddlewareNotUsed('Setup complete')

    def create_user_groups(self):
        group, created = Group.objects.get_or_create(name=UserGroup.ADMIN.value)
        if created:
            group.name = 'admin'
            group.save()
            self.set_admin_permission(group)

        group, created = Group.objects.get_or_create(name=UserGroup.COACH.value)
        if created:
            group.name = 'coach'
            group.save()

        group, created = Group.objects.get_or_create(name=UserGroup.PLAYER.value)
        if created:
            group.name = 'player'
            group.save()

    def create_users(self):

        # This user created only for test purposes as the system super user
        super_user = User.objects.create_user('super_user', 'super@gmail.com', 'super123', is_superuser=True,
                                              is_staff=True,
                                              last_login=timezone.now())
        self.add_to_group(UserGroup.ADMIN.value, super_user)

        admin = User.objects.create_user('admin', 'admin.a@gmail.com', 'admin123', last_login=timezone.now())
        self.add_to_group(UserGroup.ADMIN.value, admin)

        p1 = User.objects.create_user('andrew', 'tt@tt.com', 'andrew123', last_login=timezone.now())
        self.add_to_group(UserGroup.PLAYER.value, p1)
        self.map_to_player(p1, 2)

        c1 = User.objects.create_user('john', 'tt@tt.com', 'john123', last_login=timezone.now())
        self.add_to_group(UserGroup.COACH.value, c1)
        self.map_to_coach(c1, 1)

    def add_to_group(self, group_name, user):
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        group.save()
        self.create_profile(user)

    @staticmethod
    def create_profile(user):
        """create user profile to keep statistics"""
        profile = UserProfile()
        profile.user = user
        profile.save()

    @staticmethod
    def set_admin_permission(group):

        view_stats = Permission(name='Can view site stats', codename=GroupPermission.STATS.value,
                                content_type=ContentType.objects.get_for_model(UserProfile))
        view_stats.save()
        view_coaches = Permission(name='Can view coach details', codename=GroupPermission.COACH.value,
                                  content_type=ContentType.objects.get_for_model(Coach))
        view_coaches.save()
        group.permissions.add(view_stats)
        group.permissions.add(view_coaches)
        group.save()

    @staticmethod
    def map_to_coach(user, coach_id):
        coach = Coach.objects.get(pk=coach_id)
        coach.user = user
        coach.save()

    @staticmethod
    def map_to_player(user, player_id):
        player = Player.objects.get(pk=player_id)
        player.user = user
        player.save()
