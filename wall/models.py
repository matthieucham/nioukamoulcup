import uuid
from django.db import models
from django.contrib.auth.models import User
import re


def _find_urls_in_text(content):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls


# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    in_reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField(null=False, blank=False)
    hotlinked_content = models.URLField(max_length=2000, null=True, blank=True)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        hl_urls = _find_urls_in_text(self.message)
        if hl_urls:
            self.hotlinked_content = hl_urls[0]
        if self.in_reply_to:
            if self.in_reply_to.in_reply_to:
                self.in_reply_to = self.in_reply_to.in_reply_to
        return super(Post, self).save(*args, **kwargs)


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
