#! /usr/bin/env python
import oerplib
import pwd, os
import commands
import sys

class ServerEnviroment(object):
    '''
     Obj that allows create the enviroment for openerp such as linux user,
     postgres user and openerp config file 

     You need run this instance with root users
    '''

    def __init__(self, puser, name, password):
        '''
         >>> import pwd, os
         >>> from enviroment import ServerEnviroment
         >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
         >>> (os.getenv("SUDO_USER") or os.getenv("USER") == 'root') and '1' or '0'
         '1'

        @param puser: String with the postgres user to creater new roles
        @param name: String with new user name
        @param password: String with user password
        '''

        self.name = name
        self.password = password
        self.puser = puser



    def _check_port(self, port=22):
        '''
        Check if a port is being used for some service in the system
        >>> from enviroment import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
        >>> enviroment._check_port()
        True


        @param port: Number of port to check
        return True if the port is being used
        '''

        if commands.getoutput('lsof -i :%s' % port) or \
                commands.getoutput('lsof -i %s' % port):
            return True

        return False

    def _check_user_exists(self, name):
        '''
        This method validate if a user exist
        >>> from enviroment import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
        >>> enviroment._check_user_exists('root')
        True


        @param name: String with the name of user to search him
        return True if the user exist
        '''
        try:
            pwd.getpwnam('%s' % name)[2]
            return True
        except:
            return False

        return False

    def create_config_file(self, path_folder,  )
    def create_postgres_user(self):
        '''
        Create a user with the only role of create database
        >>> from enviroment import ServerEnviroment
        >>> import os
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
        >>> enviroment.create_postgres_user()
        True
        >>> os.system("""dropuser gerrard""")
        0

        return True if the user was created
        '''
        try:
            uid = pwd.getpwnam('%s' % self.puser)[2]
            os.setuid(uid)
            os.popen('''psql -c "CREATE USER %s 
                                 WITH PASSWORD '%s'
                                 CREATEDB" -U %s -d template1''' % \
                                                        (self.name,
                                                         self.password,
                                                         self.puser))
            return True

        except Exception, error:
            return error

        return False


    def create_linux_user(self):
        '''
        This method creates a linux user for then create a postgres user for
        him
        >>> from enviroment import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
        >>> enviroment.create_linux_user()
        True
        >>> os.system("userdel gerrard -r")
        0

        return True if the user was created
        '''
        try:
            os.system("useradd %s -m -p %s" % (self.name, self.password))
            self.user_uid = pwd.getpwnam('%s' % self.name)[2]
            return True
        except Exception, error:
            return error
        return False


if __name__ == "__main__":
    args = sys.argv
    if 'create_postgres_user' in args and len(args) == 5:
        #enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain')
        enviroment = ServerEnviroment(args[2], args[3], args[4])
        enviroment.create_postgres_user()
    else:
        import doctest
        doctest.testmod()
