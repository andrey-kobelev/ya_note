from http import HTTPStatus

from .constants_and_baseclass import (
    BaseTestClass,
    LIST_URL,
    EDIT_URL,
    ADD_URL,
)
from ..forms import NoteForm
from ..models import Note


class TestContent(BaseTestClass):

    def test_author_notes_not_availability_for_not_author(self):
        notes = self.reader_client.get(LIST_URL).context['object_list']
        self.assertFalse(
            notes.filter(pk=self.note.pk).exists()
        )

    def test_notes_list_for_author(self):
        self.assertEqual(Note.objects.count(), 1)
        response = self.author_client.get(LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        notes_from_context = response.context['object_list']
        self.assertEqual(notes_from_context.count(), 1)
        note = notes_from_context.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.note.slug)

    def test_form_is_on_pages(self):
        urls = (
            EDIT_URL,
            ADD_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
