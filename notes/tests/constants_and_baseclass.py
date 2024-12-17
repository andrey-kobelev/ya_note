from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note

NOTE_SLUG = 'note-slug'
NOTE_TEXT = 'Note text bla bla bla'
NOTE_TITLE = 'Note title'

NOTE_FORM_DATA = {
    'title': NOTE_TITLE,
    'text': NOTE_TEXT,
    'slug': NOTE_SLUG
}

NEW_FORM_DATA = {
    'title': f'{NOTE_TITLE} new',
    'text': f'{NOTE_TEXT} new',
    'slug': f'{NOTE_SLUG}-new'
}

ADD_URL = reverse('notes:add')
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
DONE_URL = reverse('notes:success')

DETAIL_URL = reverse(
    'notes:detail', args=(NOTE_SLUG,)
)
DELETE_URL = reverse(
    'notes:delete', args=(NOTE_SLUG,)
)
EDIT_URL = reverse(
    'notes:edit', args=(NOTE_SLUG,)
)

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
NEXT = '{}?next={}'

User = get_user_model()


class BaseTestClass(TestCase):

    @classmethod
    def setUpTestData(cls, create_note=True):

        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create(username='User')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        if create_note:
            cls.note = Note.objects.create(
                title=NOTE_TITLE,
                text=NOTE_TEXT,
                author=cls.author,
                slug=NOTE_SLUG
            )
