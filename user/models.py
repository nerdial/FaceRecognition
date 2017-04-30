from django.db import models
import datetime
from lib import jalali
from django.utils.timezone import localtime


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    last_id = models.IntegerField(default=0)
    create_at = models.DateTimeField(null=True)


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    type = models.CharField(max_length=200)

    def get_time(self):
        local_date = localtime(self.datetime)
        return local_date.strftime('%H:%M:%H')

    def jalali_date(self):
        return jalali.Gregorian(self.datetime.strftime('%Y/%m/%d')).persian_string('{}/{}/{}')


def create_new_log(user, type):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    now_logs = Log.objects.filter(user=user, datetime__startswith=now)
    last_log = Log.objects.filter(user=user, datetime__startswith=now).last()

    if now_logs.count() == 0:
        log = Log()
        log.user = user
        log.type = type
        log.save()
    else:
        if last_log.type == type:
            print('system compromised.. ! something is wrong with that person')
            print('last state of user : ' + user.name + ' was ' + last_log.type
                  + ' and now he is trying to  ' + type + ' again?' )
        else:
            print(user.name)
            print('new log registered for ' + type)
            log = Log()
            log.user = user
            log.type = type
            log.save()


def get_user_by_id(id):
    user = User.objects.filter(id=id)
    if user.count():
        return user.get()
    else:
        return None
