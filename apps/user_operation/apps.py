from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = "用户操作管理"

    def ready(self):    #这是根据DRF信号量做的操作。
        import user_operation.signals       #这是根据DRF信号量做的操作。
