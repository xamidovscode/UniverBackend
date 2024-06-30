from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Floor(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    is_active = models.BooleanField(default=True, verbose_name='Active')
    parent = models.ForeignKey("self", on_delete=models.PROTECT, verbose_name="Qavat", related_name='children',
                               null=True, blank=True)
    order = models.PositiveIntegerField(default=999)

    class Meta:
        verbose_name = "Qavat va Honalar"
        verbose_name_plural = "Qavat va Honalar"



