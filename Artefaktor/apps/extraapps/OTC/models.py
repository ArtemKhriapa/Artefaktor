from django.db import models
import hashlib

class OTC(models.Model):
    datetime = models.DateTimeField(auto_now_add = True)
    otc = models.CharField(max_length = 64, blank = True,  unique = True)
    is_used = models.BooleanField(default = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.otc = self.calculate(str(self.datetime))

    def calculate(self,salt):
         res = hashlib.sha256(salt.encode('utf-8'))
         return res.hexdigest()