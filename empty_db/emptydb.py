import getpass
import string
import subprocess
import random
import sys
from optparse import OptionParser, OptParseError


class EmptyDb(object):
    def __init__(self, db_driver=None, r_user=None, r_pass=None, db_name=None, db_user_name=None, db_user_pass=None,
                 db_host=None, pass_len=None):
        if db_driver is not None:
            self._driver = db_driver
        else:
            self._driver = 'mysql'
        if r_user is not None:
            self._user = r_user
        else:
            self._user = 'root'
        if r_pass is not None:
            self.__pass = r_pass
        else:
            self.__pass = None
        if pass_len is not None:
            self._pass_len = pass_len
        else:
            self._pass_len = 8
        if db_name is not None:
            self._db_name = db_name
        else:
            self._db_name = ''.join(
                random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase) for _ in
                range(self._pass_len))
        if db_user_name is not None:
            self._db_user = db_user_name
        else:
            self._db_user = '_'.join([self._db_name, 'my_user'])
        if db_host is not None:
            self._db_host = db_host
        else:
            self._db_host = 'localhost'
        if db_user_pass is not None:
            self.__db_pass = db_user_pass
        else:
            self.__db_pass = ''.join(
                random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in
                range(self._pass_len))

    @property
    def password(self):
        return self.__pass

    @password.setter
    def password(self, value):
        self.__pass = value

    @property
    def user_password(self):
        return self.__db_pass

    @user_password.setter
    def user_password(self, value):
        self.__db_pass = value

    @property
    def database(self):
        return self._db_name

    @property
    def user(self):
        return self._db_user

    def create_db(self):
        if self._driver == 'mysql':
            try:
                sql_stm = "CREATE DATABASE IF NOT EXISTS " + self._db_name + ";"
                output = subprocess.check_output(['mysql', '-u' + self._user, "-p" + self.password,
                                                  "-e " + sql_stm])
                grant_stm = "GRANT 	SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,INDEX,ALTER,CREATE TEMPORARY TABLES, CREATE VIEW,EVENT,TRIGGER,SHOW VIEW,CREATE ROUTINE,ALTER ROUTINE,EXECUTE ON `" + \
                            self._db_name + "`.* TO '" + self._db_user + \
                            "'@'" + self._db_host + "' IDENTIFIED BY '" + self.password + "';"
                output = subprocess.check_output(['mysql', '-u' + self._user, "-p" + self.password,
                                                  "-e " + grant_stm])
                return True
            except sys.stderr as error:
                print("error: " + error + " " + str(output))


def main():
    parser = OptionParser("usage: %prog [options] arg", description="Create an empty data base")
    parser.add_option("-u", "--db_user", action="store", type="string",
                      help="Database user name, random string as default")
    parser.add_option("-p", "--db_pass", action="store", type="string",
                      help="Database user password, random string as default")
    parser.add_option("-U", "--root_user", action="store", type="string",
                      help="Database server root user name")
    parser.add_option("-P", "--root_pass", action="store", type="string",
                      help="Database server user password, if none input will ask")
    parser.add_option("-H", "--host", action="store", type="string",
                      help="Database host url")
    parser.add_option("-d", "--driver", action="store", type="string",
                      help="Database driver, mysql string as default")
    parser.add_option("-l", "--length", action="store", type="string",
                      help="Database user name and pass, random string length when default")
    parser.add_option("-D", "--db_name", action="store", type="string",
                      help="Database name, random string as default")
    try:
        opts, args = parser.parse_args()
    except OptParseError as e:
        print(e)
        sys.exit(2)

    app = EmptyDb(db_driver=opts.driver, db_host=opts.host, r_user=opts.root_user, r_pass=opts.root_pass,
                  db_user_name=opts.db_user,
                  db_user_pass=opts.db_pass, pass_len=opts.length, db_name=opts.db_name)
    print("EmptyDB will create an empty database with params set by user")
    if app.password is None:
        app.password = getpass.getpass('Database server password:')
        response = app.create_db()
        if response:
            print("data base name: " + app.database)
            print("data base user name: " + app.user)
            print("Data base user password: " + app.user_password)


if __name__ == '__main__':
    main()
