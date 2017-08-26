import os
from alembic.config import CommandLine, Config

from peo.utils import get_config

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def main():
    current_dir = os.path.abspath(os.getcwd())

    try:
        alembic = CommandLine()
        alembic.parser.add_argument(
            "--app-config",
            dest="app_config",
            required=True,
            help="Config for app"
        )

        options = alembic.parser.parse_args()

        os.chdir(
            os.path.dirname(
                os.path.abspath(
                    options.config
                )
            )
        )

        app_config = get_config(options.app_config)

        if options.config == 'alembic.ini':
            options.config = os.path.join(BASE_PATH, options.config)

        cfg = Config(
            file_=options.config,
            ini_section=options.name,
            cmd_opts=options
        )

        cfg.set_main_option('script_location', str(os.path.join(BASE_PATH, 'alembic')))
        cfg.set_main_option('sqlalchemy.url', str(app_config['database']))

        if 'cmd' not in options:
            alembic.parser.error("too few arguments")
            exit(128)

        exit(alembic.run_cmd(cfg, options))
    finally:
        os.chdir(current_dir)
