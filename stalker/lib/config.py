# standard
import os


# pylint: disable=too-few-public-methods
class Config:
    def __init__(self):
        self.env_values = self._fetch(
            [
                # required
                self._add_env('SCRIPT_ID', str),
                self._add_env('SCRIPT_ACCESS_TOKEN', str),
                self._add_env('TELEGRAM_BOT_TOKEN', str),
                self._add_env('TELEGRAM_DEST_USER', str),
            ]
        )

    @staticmethod
    def _add_env(name, type_, optional=False):
        return {'name': name, 'type': type_, 'optional': optional}

    @staticmethod
    def _parse_int(data):
        try:
            return int(data)
        except ValueError:
            return None

    @staticmethod
    def _parse_list(data):
        try:
            return data.split(',')
        except AttributeError:
            return None

    @staticmethod
    def _parse_bool(data):
        if data == 'true':
            return True
        if data == 'false':
            return False

        return None

    def _parse_data(self, type_, data):
        if type_ == str:
            return data

        if type_ == int:
            return self._parse_int(data)

        if type_ == list:
            return self._parse_list(data)

        if type_ == bool:
            return self._parse_bool(data)

        return None

    def _fetch(self, envs):
        env_values = {}
        env_missing = []

        for env in envs:
            env_name = env['name']
            env_type = env['type']
            env_is_optional = env['optional']

            env_value = os.environ.get(env_name)

            if env_value is None or env_value == '':
                if env_is_optional:
                    env_values[env_name] = None
                else:
                    env_missing.append(env_name)

                continue

            parsed_env = self._parse_data(env_type, env_value)
            if parsed_env is None:
                raise TypeError(
                    'environment variable {} is not of type {}'.format(
                        env_name, env_type.__name__
                    )
                )

            env_values[env_name] = parsed_env

        if env_missing:
            raise AssertionError(
                'the following environment variables are missing: '
                '{}'.format(', '.join(env_missing))
            )

        return env_values

    def get(self, name):
        if not name in self.env_values:
            raise KeyError('unknown environment variable {}'.format(name))

        return self.env_values[name]


config = Config()
