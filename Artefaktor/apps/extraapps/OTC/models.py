from django.db import models
import hashlib

class OTC(models.Model):
    datetime = models.DateTimeField(auto_now_add = True)
    otc = models.CharField(max_length = 64, blank = True)
    is_used = models.BooleanField(default = False)

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.otc = self.calculate(str(self.datetime))

    def calculate(self,salt):
         res = hashlib.sha256(salt.encode('utf-8'))
         return res.hexdigest()

    def __str__(self):
        return "ID: %s, Time: %s, OTC: %s, Used: %s" % \
               (self.id, self.datetime, self.otc, self.is_used)