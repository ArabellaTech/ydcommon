import os
import django
import shlex
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from optparse import make_option

DUMP_COMMAND_NAME = 'mysqldump'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database which to '
                'dump.  Defaults to the "default" database.'),
        )
    help = """\
Dumps the whole database (mysql only!). Looks at the environment
variable MYSQLDUMP_OPTIONS and uses what it finds there as additional
options."""
    args = "[table1 table2 ...]"

    requires_model_validation = False

    def handle(self, *args, **kwargs):
        connection = connections[kwargs.get('database', DEFAULT_DB_ALIAS)]
        settings_dict = connection.settings_dict
        cmd_args = [DUMP_COMMAND_NAME]
        db = settings_dict['OPTIONS'].get('db', settings_dict['NAME'])
        user = settings_dict['OPTIONS'].get('user', settings_dict['USER'])
        passwd = settings_dict['OPTIONS'].get('passwd', settings_dict['PASSWORD'])
        host = settings_dict['OPTIONS'].get('host', settings_dict['HOST'])
        port = settings_dict['OPTIONS'].get('port', settings_dict['PORT'])

        if user:
            cmd_args += ["--user=%s" % user]
        if passwd:
            cmd_args += ["--password=%s" % passwd]
        if host:
            cmd_args += ["--host=%s" % host]
        if port:
            cmd_args += ["--port=%s" % port]

        cmd_args.extend(shlex.split(os.getenv("MYSQLDUMP_OPTIONS", '')))

        if len(args):
            tables = list(args)
        else:
            tables = connection.introspection.get_table_list(connection.cursor())

        if django.VERSION >= (1, 8):
            cmd_args += ["--extended-insert", db] + [str(t.name) for t in tables]
        else:
            cmd_args += ["--extended-insert", db] + tables

        try:
            if os.name == 'nt':
                sys.exit(os.system(" ".join(cmd_args)))
            else:
                os.execvp(DUMP_COMMAND_NAME, cmd_args)
        except OSError:
            # Note that we're assuming OSError means that the client program
            # isn't installed. There's a possibility OSError would be raised
            # for some other reason, in which case this error message would be
            # inaccurate. Still, this message catches the common case.
            raise CommandError('You appear not to have the %r program installed or on your path.' % DUMP_COMMAND_NAME)
