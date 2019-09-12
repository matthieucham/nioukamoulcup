import uuid
from django.db import models
from django.contrib.auth.models import User
import re
import requests
import imghdr
from PIL import Image
from io import BytesIO


def _find_urls_in_text(content):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls


def _is_url_of_picture(url):
    try:
        img = requests.get(url)
        # check status code
        if img.status_code != 200:
            return False  # url invalide
        whattype = imghdr.what(None, h=img.content)
        if whattype is not None:
            return True
        # Test with PIL because imghdr misses some formats
        try:
            img = Image.open(BytesIO(requests.get(url).content))
            img.verify()
            return True  # valid image
        except Exception:
            return False  # invalid image

    except Exception:
        return False


def _extract_hotlinked_picture(urls):
    if not urls:
        return None
    for url in urls:
        if _is_url_of_picture(url):
            return url
    # Aucune image trouvée: on repart pour un tour en scraping cette fois
    from bs4 import BeautifulSoup as BS
    min_size = 50  # min pour une bonne image ?
    for url in urls:
        try:
            page = requests.get(url)
            soup = BS(page.text)
            for imgtag in soup.find_all('img'):
                imgsrc = imgtag['src']
                if _is_url_of_picture(imgsrc):
                    im = Image.open(BytesIO(requests.get(imgsrc).content))
                    w, h = im.size
                    if w > min_size and h > min_size:
                        return imgsrc
        except Exception as e:
            continue  # on passe au lien suivant si celui ci ne fonctionne pas
    return None


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
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        hl_urls = _find_urls_in_text(self.message)
        if hl_urls:
            self.hotlinked_picture = _extract_hotlinked_picture(hl_urls)
        if self.in_reply_to:
            if self.in_reply_to.in_reply_to:
                self.in_reply_to = self.in_reply_to.in_reply_to
        self.edited = self.pk is not None
        self.message_blueprint = uuid.uuid3(uuid.NAMESPACE_URL, self.message)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['author', 'message_blueprint']]


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
