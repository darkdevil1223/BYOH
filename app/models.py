from django.db import models

class ServerRequest(models.Model):
    full_name = models.CharField(max_length=100)
    ldap = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    extension_number = models.CharField(max_length=20)
    server_name = models.CharField(max_length=100)
    number_of_servers = models.PositiveIntegerField()
    rack_space_units = models.PositiveIntegerField()
    power_per_server = models.DecimalField(max_digits=6, decimal_places=2)
    cpu_gpu_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

