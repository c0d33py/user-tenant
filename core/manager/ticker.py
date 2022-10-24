from django.db import models


class TickerQuerySet(models.QuerySet):
    ''' queryset manager using is_archive field , published field and on_air field '''

    def on_air(self):
        '''
        On Air is only work with published object
        '''
        return self.filter(draft=True).filter(on_air=True)

    def published(self):
        '''
        GET is_archive && published objects
        '''
        return self.filter(draft=True)


class TickerManager(models.Manager):
    ''' model queryset mangager for a archive model '''

    def get_queryset(self):
        return TickerQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def on_air(self):
        return self.get_queryset().on_air()
