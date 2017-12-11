from django.db import models
import hashlib as hash
from datetime import datetime

class OTC(models.Model):

    otc = models.CharField(max_length = 64, blank = True,  unique = True)
    is_used = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if self.is_used == False:
            flag = True
            while flag:
                try:
                    dt = str(datetime.now())
                    otc = hash.sha256(dt.encode('utf-8'))
                    self.otc = otc.hexdigest()
                    super().save(*args, **kwargs)
                    flag = False
                except Exception as e:
                    pass
        else:
            super().save(*args, **kwargs)