"""Offline-only regression tests; no provider credentials or connections."""
import ast
import importlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch

config = importlib.import_module('mxonline.runtime_config')
ROOT = Path(__file__).resolve().parents[1]


class ConfigurationTests(unittest.TestCase):
    def test_missing_value_fails_without_secret(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'UNIT_TEST_REQUIRED'):
                config.required_env('UNIT_TEST_REQUIRED')

    def test_blank_value_fails(self):
        with patch.dict(os.environ, {'UNIT_TEST_REQUIRED': '  '}, clear=True):
            with self.assertRaises(RuntimeError):
                config.required_env('UNIT_TEST_REQUIRED')

    def test_supplied_value_is_used(self):
        with patch.dict(os.environ, {'UNIT_TEST_REQUIRED': 'offline-fixture'}, clear=True):
            self.assertEqual(config.required_env('UNIT_TEST_REQUIRED'), 'offline-fixture')

    def test_sources_compile(self):
        for name in ['mxonline/settings.py', 'mxonline/runtime_config.py', 'utils/email_send.py']:
            compile((ROOT / name).read_bytes(), name, 'exec')


    def test_django_settings_use_environment(self):
        import runpy
        values = {'DJANGO_SECRET_KEY': 'offline-django-secret',
                  'DJANGO_DB_USER': 'offline-user', 'DJANGO_DB_PASSWORD': 'offline-db'}
        with patch.dict(os.environ, values, clear=True):
            settings = runpy.run_path(str(ROOT / 'mxonline/settings.py'))
        self.assertEqual(settings['SECRET_KEY'], values['DJANGO_SECRET_KEY'])
        self.assertEqual(settings['DATABASES']['default']['PASSWORD'], values['DJANGO_DB_PASSWORD'])
        self.assertEqual(settings['DATABASES']['default']['USER'], values['DJANGO_DB_USER'])

    def test_mail_auth_and_notification_require_config(self):
        tree = ast.parse((ROOT / 'utils/email_send.py').read_text())
        names = {node.args[0].value for node in ast.walk(tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                 and node.func.id == 'required_env'}
        self.assertTrue({'SMTP_USER', 'SMTP_PASSWORD', 'SMTP_HOST', 'SERVERCHAN_SEND_KEY'} <= names)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'set_debuglevel':
                self.assertEqual(node.args[0].value, 0)

    def test_missing_mail_config_does_not_connect(self):
        source = ast.parse((ROOT / 'utils/email_send.py').read_text())
        function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'send_mail')
        namespace = {'os': os, 'required_env': config.required_env}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'mail-test', 'exec'), namespace)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'SMTP_USER'):
                namespace['send_mail']('offline', 'offline', 'example@example.invalid')

    def test_missing_notification_config_does_not_connect(self):
        source = ast.parse((ROOT / 'utils/email_send.py').read_text())
        function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'send_wechat')
        namespace = {'required_env': config.required_env}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'notification-test', 'exec'), namespace)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'SERVERCHAN_SEND_KEY'):
                namespace['send_wechat']('offline', 'offline')

    def test_configured_mail_uses_supplied_credentials_without_debug(self):
        from unittest.mock import Mock
        source = ast.parse((ROOT / 'utils/email_send.py').read_text())
        function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'send_mail')
        smtp = Mock()
        from email.header import Header
        from email.mime.text import MIMEText
        namespace = {'os': os, 'required_env': config.required_env, 'smtplib': smtp,
                     'Header': Header, 'MIMEText': MIMEText, '_format_addr': lambda value: value}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'mail-test', 'exec'), namespace)
        values = {'SMTP_HOST': 'example.invalid', 'SMTP_USER': 'offline@example.invalid',
                  'SMTP_PASSWORD': 'offline-fixture', 'SMTP_FROM': 'sender@example.invalid'}
        with patch.dict(os.environ, values, clear=True):
            result = namespace['send_mail']('offline', 'offline', 'receiver@example.invalid')
        self.assertEqual(result, 1)
        smtp.SMTP_SSL.assert_called_once_with('example.invalid', 465, timeout=10)
        smtp.SMTP_SSL.return_value.login.assert_called_once_with(values['SMTP_USER'], values['SMTP_PASSWORD'])
        smtp.SMTP_SSL.return_value.set_debuglevel.assert_called_once_with(0)
