from http import HTTPStatus

from .constants_and_baseclass import (
    BaseTestClass,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    DETAIL_URL,
    HOME_URL,
    EDIT_URL,
    DELETE_URL,
    LIST_URL,
    ADD_URL,
    DONE_URL,
    NEXT
)


class TestRoutes(BaseTestClass):

    def test_pages_availability_for_diff_users(self):
        client_urls_status = (
            (self.client, LOGIN_URL, HTTPStatus.OK),
            (self.client, LOGOUT_URL, HTTPStatus.OK),
            (self.client, SIGNUP_URL, HTTPStatus.OK),
            (self.client, HOME_URL, HTTPStatus.OK),
            (self.reader_client, DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, DELETE_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, DETAIL_URL, HTTPStatus.OK),
            (self.author_client, DELETE_URL, HTTPStatus.OK),
            (self.author_client, EDIT_URL, HTTPStatus.OK),
            (self.author_client, LIST_URL, HTTPStatus.OK),
            (self.author_client, DONE_URL, HTTPStatus.OK),
            (self.author_client, ADD_URL, HTTPStatus.OK),
        )

        for client, url, status in client_urls_status:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect(self):
        url_redirect_url = (
            (LIST_URL, NEXT.format(LOGIN_URL, LIST_URL)),
            (DONE_URL, NEXT.format(LOGIN_URL, DONE_URL)),
            (ADD_URL, NEXT.format(LOGIN_URL, ADD_URL)),
            (DETAIL_URL, NEXT.format(LOGIN_URL, DETAIL_URL)),
            (DELETE_URL, NEXT.format(LOGIN_URL, DELETE_URL)),
            (EDIT_URL, NEXT.format(LOGIN_URL, EDIT_URL)),
        )
        for url, redirect_url in url_redirect_url:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect_url)
