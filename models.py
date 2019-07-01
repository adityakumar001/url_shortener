from django.db import models


# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=1024, null=False, default='password')
    email = models.CharField(max_length=255, null=False, unique=True, default="sample@smaple.com")
    name = models.CharField(max_length=255, null=False, default="First Last")


class URLModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    userGenerated = models.BooleanField(default=False)
    shortened_url = models.CharField(max_length=50, null=False, unique=True, default="tinyme.com/iPhoneXR64Red")
    original_url = models.CharField(max_length=1024, null=False,
                                    default="https://www.amazon.com/dp/B07K97BQDF?aaxitk=mgYRcOvalCbHqJte1Wg4Ug&pd_rd_i"
                                            "=B07K97BQDF&pf_rd_p=3fade48a-e699-4c96-bf08-bb772ac0e242&hsa_cr_id=3463342"
                                            "080701&sb-ci-n=productDescription&sb-ci-v=Apple%20iPhone%20XR%20(64GB)%20-"
                                            "%20Red%20-%20%5Bworks%20exclusively%20with%20Simple%20Mobile%5D")

    def __str__(self):
        return str(self.id) + "\t" + str(self.timestamp) + str(self.shortened_url)
