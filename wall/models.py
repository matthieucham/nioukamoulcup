import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import re
import requests
from PIL import Image
from io import BytesIO


def _find_urls_in_text(content):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls


def _is_url_of_picture(url, min_size=150):
    try:
        img = requests.get(url)
        # check status code
        if img.status_code != 200:
            return False  # url invalide
        # Test with PIL because imghdr misses some formats
        try:
            im = Image.open(BytesIO(requests.get(url).content))
            w, h = im.size
            if w > min_size and h > min_size:
                return True  # valid image
            return False  # too small image
        except Exception:
            return False  # invalid image

    except Exception:
        return False


def _extract_hotlinked_title_and_pic(url):
    from bs4 import BeautifulSoup as BS
    page = requests.get(url)
    soup = BS(page.text)
    title = None
    for htag in soup.find_all('h1'):
        if htag.text and len(htag.text.strip()) > 0:
            title = htag.text.strip()
            break
    for imgtag in soup.find_all('img'):
        imgsrc = imgtag.get('src')
        if imgsrc and _is_url_of_picture(imgsrc):
            return title, imgsrc
    return title, None


def _extract_hotlink_data(content):
    # Are there any url in content ?
    urls = _find_urls_in_text(content)
    if not urls:
        return None, None, None, content.strip()
    c = content.strip()
    # strip urls from code
    for u in urls:
        c = c.replace(u, '')
    url = urls[0]
    # extract data from url
    if _is_url_of_picture(url):
        return None, url, None, c

    t, p = _extract_hotlinked_title_and_pic(url)
    return url, p, t, c


# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    in_reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField(null=False, blank=False, max_length=2000)
    message_blueprint = models.UUIDField(blank=True)  # protect against multi_submit
    hotlinked_picture = models.URLField(max_length=2000, null=True, blank=True)
    hotlinked_url = models.URLField(max_length=2000, null=True, blank=True)
    hotlinked_title = models.CharField(max_length=200, null=True, blank=True)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        safe_msg = strip_tags(self.message)
        hl_url, hl_pic, hl_tit, clean_msg = _extract_hotlink_data(safe_msg)
        self.hotlinked_url = hl_url
        self.hotlinked_picture = hl_pic
        self.hotlinked_title = hl_tit
        self.message = clean_msg.strip()
        if self.in_reply_to:
            if self.in_reply_to.in_reply_to:
                self.in_reply_to = self.in_reply_to.in_reply_to
        self.edited = not self._state.adding
        self.message_blueprint = uuid.uuid3(uuid.NAMESPACE_URL, safe_msg)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['author', 'message_blueprint']]
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
