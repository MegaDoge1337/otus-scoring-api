import datetime
import functools
import hashlib
import unittest
from unittest.mock import Mock

import api
from store import RedisStore


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)

        return wrapper

    return decorator


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = Mock(RedisStore)
        self.request_body_template = {
            "account": None,
            "login": None,
            "method": None,
            "token": None,
            "arguments": None,
        }

    def generate_valid_user_token(self, account, login):
        digest = hashlib.sha512(
            (account + login + api.SALT).encode("utf-8")
        ).hexdigest()

        return digest

    def generate_valid_admin_token(self):
        digest = hashlib.sha512(
            (datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).encode(
                "utf-8"
            )
        ).hexdigest()

        return digest

    def create_method_request(
        self, account, login, token, method="test", arguments=None
    ):
        request_body = self.request_body_template.copy()
        request_body["account"] = account
        request_body["login"] = login
        request_body["method"] = method
        request_body["token"] = token
        request_body["arguments"] = {} if not arguments else arguments

        return api.MethodRequest(request_body)

    def get_response(self, request):
        return api.method_handler(
            {"body": request, "headers": self.headers}, self.context, self.store
        )

    @cases([("account", "login")])
    def test_valid_user_auth(self, account, login):
        token = self.generate_valid_user_token(account, login)
        request = self.create_method_request(account, login, token)

        self.assertEqual(api.check_auth(request), True)
        self.assertEqual(request.is_admin, False)

    @cases(
        [
            ("account", "login", None),
            ("account", "login", ""),
            ("account", "login", "token"),
            ("account", "login", "94a08da1fecbb6e8b46990538c7b50b2"),
            ("account", "login", "ee977806d7286510da8b9a7492ba58e2484c0ecc"),
        ]
    )
    def test_invalid_user_auth(self, account, login, token):
        request = self.create_method_request(account, login, token)

        self.assertEqual(api.check_auth(request), False)

    @cases([("account", "admin")])
    def test_valid_admin_auth(self, account, login):
        token = self.generate_valid_admin_token()
        request = self.create_method_request(account, login, token)

        self.assertEqual(api.check_auth(request), True)
        self.assertEqual(request.is_admin, True)

    @cases(
        [
            ("account", "admin", None),
            ("account", "admin", ""),
            ("account", "admin", "token"),
            ("account", "admin", "94a08da1fecbb6e8b46990538c7b50b2"),
            ("account", "admin", "ee977806d7286510da8b9a7492ba58e2484c0ecc"),
        ]
    )
    def test_invalid_admin_auth(self, account, login, token):
        request = self.create_method_request(account, login, token)

        self.assertEqual(api.check_auth(request), False)

    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    def test_method_invalid_request(self):
        pass

    def test_client_interests_valid_request(self):
        pass

    def test_client_interests_invalid_request(self):
        pass

    def test_client_interests_context(self):
        pass

    def test_online_score_valid_request(self):
        pass

    def test_online_score_admin_valid_request(self):
        pass

    def test_online_score_invalid_request(self):
        pass

    def test_online_score_context(self):
        pass


if __name__ == "__main__":
    unittest.main()
