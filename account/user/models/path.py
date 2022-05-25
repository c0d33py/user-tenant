import os
from datetime import datetime


def set_filename_format(now, instance, filename):
    return '{date}-{microsecond}{extension}'.format(
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def file_path(instance, filename):
    now = datetime.now()

    path = 'profile/{user}/{year}/{filename}'.format(
        user=instance.user.username,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance, filename),
    )
    return path
