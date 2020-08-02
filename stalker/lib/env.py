import os


class Environment:
    def __init__(self):
        self.env_values = Environment.fetch([
            Environment.add_env('SCRIPT_ID', str),
            Environment.add_env('SCRIPT_ACCESS_TOKEN', str),
            Environment.add_env('TELEGRAM_BOT_TOKEN', str),
            Environment.add_env('TELEGRAM_DEST_USER', str),
        ])

    @staticmethod
    def add_env(name, type_):
        return {'name': name, 'type': type_}

    @staticmethod
    def fetch(envs):
        env_values = {}

        missing = []
        for env in envs:
            env_name = env['name']
            env_type = env['type']
            env_value = os.environ.get(env_name)

            if env_value is None:
                missing.append(env_name)
            else:
                if env_type == int:
                    try:
                        env_values[env_name] = int(env_value)
                    except ValueError:
                        raise Exception(
                            'environment variable {} is not of type {}'.format(
                                env_name, env_type.__name__))
                else:
                    env_values[env_name] = env_value

        if missing:
            raise Exception('the following environment variables are missing: '
                            '{}'.format(', '.join(missing)))

        return env_values

    def get(self, name):
        env = self.env_values.get(name)
        if env is None:
            raise Exception('unknown environment variable {}'.format(name))

        return env


environment = Environment()
