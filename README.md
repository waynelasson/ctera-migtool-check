# ctera-migtool-check
CTERASDK scripts

Usage: ctera-miglog-check.py [OPTIONS]

  Check for migration log errors

Options:
  -a, --address TEXT  Edge filer FQDN  [required]
  -u, --admin TEXT    Edge filer admin user  [required]
  -j, --job TEXT      Migration job number  [required]
  --debug             debug
  --help              Show this message and exit.

Example:

py ctera-miglog-check.py -a teancum01.ctera.me -u admin -j 1
2023-11-22 10:28:28,978    INFO [login.py:19] [login] - User logged in. {'host': 'teancum01.ctera.me', 'user': 'admin'}
2023-11-22 10:28:29,129    INFO [telnet.py:16] [enable] - Enabling telnet access.
2023-11-22 10:28:29,141    INFO [telnet.py:25] [enable] - Telnet access enabled.
/var/volumes/vol1/.ctera/migrationlogs/jobs/1/
2023-11-22 10:28:29,142    INFO [shell.py:19] [run_command] - Executing shell command. {'shell_command': 'grep sender /var/volumes/vol1/.ctera/migrationlogs/jobs/1/migration.log | grep rsync | grep -v vanished'}
2023-11-22 10:28:31,308    INFO [shell.py:26] [run_command] - Shell command executed. {'shell_command': 'grep sender /var/volumes/vol1/.ctera/migrationlogs/jobs/1/migration.log | grep rsync | grep -v vanished'}
2023-11-22 10:28:31,308    INFO [telnet.py:29] [disable] - Disabling telnet access.
2023-11-22 10:28:31,321    INFO [telnet.py:31] [disable] - Telnet access disabled.
2023-11-22 10:28:31,335    INFO [login.py:30] [logout] - User logged out. {'host': 'teancum01.ctera.me', 'user': 'admin'}

        Log File: output\teancum01-2023_11_22-10-28.csv
