from http import HTTPStatus
from pytils.translit import slugify

from .constants_and_baseclass import (
    BaseTestClass,
    EDIT_URL,
    DONE_URL,
    DELETE_URL,
    ADD_URL,
    LOGIN_URL,
    NEW_FORM_DATA,
    NOTE_FORM_DATA
)
from notes.models import Note
from notes.forms import WARNING


class TestLogic(BaseTestClass):

    def create_note_for_author(self, form_data=NOTE_FORM_DATA):
        Note.objects.all().delete()
        self.assertEqual(Note.objects.count(), 0)
        response = self.author_client.post(
            ADD_URL,
            data=form_data
        )
        self.assertRedirects(response, DONE_URL)
        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.last()

        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.author, self.author)
        if 'slug' in form_data.keys():
            self.assertEqual(note.slug, form_data['slug'])
        else:
            self.assertEqual(note.slug, slugify(note.title))

    def test_author_can_create_notes(self):
        self.create_note_for_author()

    def test_anonym_cant_create_note(self):
        notes = sorted(Note.objects.all())
        redirect_url = f'{LOGIN_URL}?next={ADD_URL}'
        response = self.client.post(
            ADD_URL,
            data=NEW_FORM_DATA
        )
        self.assertRedirects(response, redirect_url)
        self.assertEqual(
            sorted(Note.objects.all()), notes
        )

    def test_same_slug_dont_create(self):
        notes = sorted(Note.objects.all())
        response = self.author_client.post(
            ADD_URL,
            data=NOTE_FORM_DATA
        )
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{NOTE_FORM_DATA["slug"]}{WARNING}'
        )
        self.assertEqual(
            sorted(Note.objects.all()), notes
        )

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            EDIT_URL,
            data=NEW_FORM_DATA
        )
        self.assertRedirects(response, DONE_URL)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, NEW_FORM_DATA['title'])
        self.assertEqual(note.text, NEW_FORM_DATA['text'])
        self.assertEqual(note.slug, NEW_FORM_DATA['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_another_user_cant_edit_note(self):
        notes_count = Note.objects.count()
        response = self.reader_client.post(
            EDIT_URL,
            data=NEW_FORM_DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, DONE_URL)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_another_user_cant_delete_note(self):
        response = self.reader_client.delete(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.note.slug)

    def test_empty_slug(self):
        form_data = NOTE_FORM_DATA.copy()
        form_data.pop('slug')
        self.create_note_for_author(form_data=form_data)
