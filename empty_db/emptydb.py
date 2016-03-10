import getpass
import string
import subprocess
import random
import sys
import getopt


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


def main(argv):
    db_user = None
    db_pass = None
    dbname = None
    root_user = None
    root_pass = None
    host = None
    driver = None
    pass_length = None
    try:
        opts, args = getopt.getopt(argv, 'hu:p:U:P:H:d:l:D:',
                                   ['db_user=', 'db_pass=', 'root_user=', 'root_pass=', 'host=', 'driver=', 'length=',
                                    'db_name='])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                "EmptyDB Creates an empty Database with given params \n "
                "-u or --db_user Database user name, random string as default \n "
                "-p or --db_pass Database user pass, random string as default \n "
                "-U or --root_user Database server root user \n "
                "-P or --root_pass Database root password \n -H or --host Database host address \n "
                "-d or --driver Server host, mysql as default \n "
                "-l or --length Database user password length, 8 char as default \n"
                "-D or --db_name for Database name, random string as default")
            sys.exit(0)
        if opt in ('-u', '--db_user'):
            db_user = arg
        if opt in ('-p', '--db_pass'):
            db_pass = arg
        if opt in ('-U', '--root_user'):
            root_user = arg
        if opt in ('-P', '--root_pass'):
            root_pass = arg
        if opt in ('-H', '--host'):
            host = arg
        if opt in ('-d', '--driver'):
            driver = arg
        if opt in ('-l', '--length'):
            pass_length = arg
        if opt in ('-D', '--db_name'):
            dbname = arg

    app = EmptyDb(db_driver=driver, db_host=host, r_user=root_user, r_pass=root_pass, db_user_name=db_user,
                  db_user_pass=db_pass, pass_len=pass_length, db_name=dbname)
    print("EmptyDB will create an empty database with params set by user")
    if app.password is None:
        app.password = getpass.getpass('Database server password:')
        response = app.create_db()
        if response:
            print("data base name: " + app.database)
            print("data base user name: " + app.user)
            print("Data base user password: " + app.user_password)


if __name__ == '__main__':
    main(sys.argv[1:])
