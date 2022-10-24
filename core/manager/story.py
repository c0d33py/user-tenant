from django.db import models


class ArticleQuerySet(models.Manager):
    def get_queryset(self):
        return super(ArticleQuerySet, self).get_queryset().filter(status=True)


class PersonQuerySet(models.QuerySet):
    def Pending(self):
        return self.filter(approvel='Pending')

    def Appropriate(self):
        return self.filter(approvel='Appropriate')

    def Approved(self):
        return self.filter(approvel='Approved')


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def Pending(self):
        return self.get_queryset().Pending()

    def Appropriate(self):
        return self.get_queryset().Appropriate()

    def Approved(self):
        return self.get_queryset().Approved()
