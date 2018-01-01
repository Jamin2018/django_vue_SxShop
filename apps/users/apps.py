from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"

    def ready(self):    #这是根据DRF信号量做的操作。
        import users.signals    #这是根据DRF信号量做的操作。