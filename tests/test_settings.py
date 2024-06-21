from django.test import TestCase, override_settings

<<<<<<< HEAD
from drf_comments.settings import APISettings, api_settings
=======
from rest_framework.settings import APISettings, api_settings
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


class TestSettings(TestCase):
    def test_import_error_message_maintained(self):
        """
        Make sure import errors are captured and raised sensibly.
        """
        settings = APISettings({
            'DEFAULT_RENDERER_CLASSES': [
                'tests.invalid_module.InvalidClassName'
            ]
        })
        with self.assertRaises(ImportError):
            settings.DEFAULT_RENDERER_CLASSES

    def test_warning_raised_on_removed_setting(self):
        """
        Make sure user is alerted with an error when a removed setting
        is set.
        """
        with self.assertRaises(RuntimeError):
            APISettings({
                'MAX_PAGINATE_BY': 100
            })

    def test_compatibility_with_override_settings(self):
        """
        Ref #5658 & #2466: Documented usage of api_settings
        is bound at import time:

<<<<<<< HEAD
            from drf_comments.settings import api_settings
=======
            from rest_framework.settings import api_settings
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9

        setting_changed signal hook must ensure bound instance
        is refreshed.
        """
        assert api_settings.PAGE_SIZE is None, "Checking a known default should be None"

        with override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10}):
            assert api_settings.PAGE_SIZE == 10, "Setting should have been updated"

        assert api_settings.PAGE_SIZE is None, "Setting should have been restored"

    def test_pagination_settings(self):
        """
        Integration tests for pagination system check.
        """
<<<<<<< HEAD
        from drf_comments.checks import pagination_system_check
=======
        from rest_framework.checks import pagination_system_check
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9

        def get_pagination_error(error_id: str):
            errors = pagination_system_check(app_configs=None)
            return next((error for error in errors if error.id == error_id), None)

        self.assertIsNone(api_settings.PAGE_SIZE)
        self.assertIsNone(api_settings.DEFAULT_PAGINATION_CLASS)

<<<<<<< HEAD
        pagination_error = get_pagination_error('drf_comments.W001')
        self.assertIsNone(pagination_error)

        with override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10}):
            pagination_error = get_pagination_error('drf_comments.W001')
            self.assertIsNotNone(pagination_error)

        default_pagination_class = 'drf_comments.pagination.PageNumberPagination'
        with override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10, 'DEFAULT_PAGINATION_CLASS': default_pagination_class}):
            pagination_error = get_pagination_error('drf_comments.W001')
=======
        pagination_error = get_pagination_error('rest_framework.W001')
        self.assertIsNone(pagination_error)

        with override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10}):
            pagination_error = get_pagination_error('rest_framework.W001')
            self.assertIsNotNone(pagination_error)

        default_pagination_class = 'rest_framework.pagination.PageNumberPagination'
        with override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10, 'DEFAULT_PAGINATION_CLASS': default_pagination_class}):
            pagination_error = get_pagination_error('rest_framework.W001')
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
            self.assertIsNone(pagination_error)


class TestSettingTypes(TestCase):
    def test_settings_consistently_coerced_to_list(self):
        settings = APISettings({
<<<<<<< HEAD
            'DEFAULT_THROTTLE_CLASSES': ('drf_comments.throttling.BaseThrottle',)
=======
            'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.BaseThrottle',)
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
        })
        self.assertTrue(isinstance(settings.DEFAULT_THROTTLE_CLASSES, list))

        settings = APISettings({
            'DEFAULT_THROTTLE_CLASSES': ()
        })
        self.assertTrue(isinstance(settings.DEFAULT_THROTTLE_CLASSES, list))
