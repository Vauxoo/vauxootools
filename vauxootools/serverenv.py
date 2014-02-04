#!/usr/bin/env python
import pwd, os
import commands
import sys
import ConfigParser
import openerp
import random

class ServerEnviroment(object):
    '''
     Obj that allows create the enviroment for openerp such as linux user,
     postgres user and openerp config file

     You need run this instance with root users
    '''

    def __init__(self, puser, name, password, addons_path, config_folder,
                 server_path):
        '''
         >>> import pwd, os
         >>> from serverenv import ServerEnviroment
         >>> enviroment = ServerEnviroment('postgres', 'gerrard',
         ...                               'thecaptain', '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
         >>> (os.getenv("SUDO_USER") or os.getenv("USER") == 'root') and \
                                                                 '1' or '0'
         '1'

        @param puser: String with the postgres user to creater new roles
        @param name: String with new user name
        @param password: String with user password
        '''

        self.name = name
        self.password = password
        self.puser = puser
        self.addons_path = addons_path
        self.config_folder = config_folder
        self.server_path = server_path
        self.user_uid = 0
        self.port = 8069
        self.database = False


    @staticmethod
    def _check_port(port=22):
        '''
        Check if a port is being used for some service in the system
        >>> from serverenv import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        
        #Check if port by default(22) is run in the server

        >>> enviroment._check_port()
        True


        @param port: Number of port to check
        return True if the port is being used
        '''

        if commands.getoutput('lsof -i :%s' % port):
            return True

        return False

    @staticmethod
    def _check_user_exists(name):
        '''
        This method validate if a user exist
        >>> from serverenv import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment._check_user_exists('root')
        0


        @param name: String with the name of user to search him
        return True if the user exist
        '''
        try:
            return pwd.getpwnam('%s' % name)[2]
        except:
            return False

        return False

    def _get_available_port(self, port, opt, key=None):
        '''
        Return a port available in the system
        >>> from serverenv import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment._get_available_port(9876, 'xmlrpc_port')
        9876

        '''
        name_port = opt.split('_')
        if len(name_port[0]) > 5:
            port = key and port or random.randrange(0, 65535)
            if not self._check_port(port):
                return port
            else:
                new_port = random.randrange(0, 65535)
                return self._get_available_port(new_port, opt, True)
        else:
            return port

        return True


    def create_config_file(self):
        '''
        This method validate if a user exist

        >>> from serverenv import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment.create_config_file()
        True
        >>> os.system('rm /tmp/gerrard_config_file')
        0
        '''
        config = ConfigParser.ConfigParser()
        config.add_section('options')
        option = openerp.tools.config
        options = option.options
        options2 = options.copy()
        for opt in options2:
            if 'port' in opt:
                port = str(self._get_available_port(options[opt], opt))
                config.set('options', opt, port)
                if opt == 'xmlrpc_port':
                    self.port = port

            elif opt in ('translate_in', 'translate_out'):
                continue

            else:
                config.set('options', opt, str(options[opt]))

        os.setuid(self.user_uid)
        config.set('options','addons_path', self.addons_path)
        config.set('options','db_password', self.password)
        config.set('options','db_user', self.name)
        config.set('options','netrpc', False)
        config.set('options','xmlrpc', True)
        config.set('options','log_handler', "[':INFO']")
        config.set('options','xmlrpcs', True)
        config.set('options','db_lang', 'es_MX')
        config.set('options','db_name',False)
        try:
            f_name = '%s/%s_config_file' % (self.config_folder,
                                            self.name.lower())
            f_copy = '%s/%s_config_file' % (self.config_folder,
                                            'copy_of_god')
            os.system('touch %s' % f_name )
            config_file = file(f_name, 'w')
            config.write(config_file)
            config_file.close()
            c_file = open(f_name, 'r')
            copy_file = open(f_copy, 'w')
            no_conf = ['publisher_warranty_url', 'save', 'init',
                       'stop_after_init', 'overwrite_existing_translations',
                       'reportgz', 'db_lang', 'db_maxconn', 
                       'config', 'language', 'update', 'root_path']
            for line in c_file.readlines():
                if not all([False for i in no_conf if i in line]) and \
                    'addons_path' not in line:
                    continue    
                elif line.find('import_partial') >= 0:
                    copy_file.write('import_partial = \n')
                else:
                    copy_file.write(line)

            c_file.close()
            copy_file.close()
            os.popen('mv %s %s' % (f_copy, f_name))
            return True

        except Exception, error:
            print 'eeeeeeeeeeeeeeeerrrrrrrrrrrroooooooooor', error
            return error

        return False
    def create_postgres_user(self):
        '''
        Create a user with the only role of create database
        >>> from serverenv import ServerEnviroment
        >>> import os
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> os.popen('python enviroment.py create_postgres_user  postgres gerrard thecaptain') and True
        True

        return True if the user was created
        '''
        try:
            uid = pwd.getpwnam('%s' % self.puser)[2]
            os.setuid(uid)
            if self.name == 'liverpool':
                os.popen('dropuser gerrard')
            else:
                os.popen('''psql -c "CREATE USER %s
                                     WITH PASSWORD '%s'
                                     CREATEDB" -U %s -d template1''' % \
                                                            (self.name,
                                                             self.password,
                                                             self.puser))


            return True

        except Exception, error:
            print 'eeeeeeeeeeeeeeee', error
            return error

        return False



    def create_linux_user(self):
        '''
        This method creates a linux user for then create a postgres user for
        him
        >>> from serverenv import ServerEnviroment
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...                               '', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment.create_linux_user()
        True
        >>> os.system("userdel gerrard -r")
        0

        return True if the user was created
        '''
        try:
            os.system("useradd %s -g cfdi_group -m -p %s" % (self.name, self.password))
            self.user_uid = pwd.getpwnam('%s' % self.name)[2]
            return True
        except Exception, error:
            return error
        return False


    def create_database(self, name):
        '''
        Create a database with psql command
        >>> from serverenv import ServerEnviroment
        >>> import os
        >>> from datetime import datetime
        >>> today = datetime.today()
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...  '/home/openerp/instancias/estable/agrinos/openobject-addons,/home/openerp/instancias/estable/agrinos/openerp-web/addons', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment.create_database()
        True
        '''
        try:
            os.popen(''' psql -c "CREATE DATABASE %s
                                     WITH OWNER %s 
                                          ENCODING 'UTF-8'
                                          TEMPLATE template1" -d template1''' \
                                                  %  (name, self.name))
            self.database = name
            return True
        except Exception, error:
            return error

        return False
    def run_server(self):
        '''
        Raises the new server with new user
        >>> from serverenv import ServerEnviroment
        >>> import os
        >>> from datetime import datetime
        >>> today = datetime.today()
        >>> path = os.path.realpath('enviroment.py')
        >>> os.system('(crontab -l; echo "%s %s %s %s * %s prueba clean") | crontab' % ((today.minute+1), today.hour, today.day, today.month, path)) and True
        0
        >>> enviroment = ServerEnviroment('postgres', 'gerrard', 'thecaptain',
        ...  '/home/openerp/instancias/estable/agrinos/openobject-addons,/home/openerp/instancias/estable/agrinos/openerp-web/addons', '/tmp', '/home/openerp/instancias/estable/agrinos/server')
        >>> enviroment.create_linux_user()
        True
        >>> enviroment.create_config_file()
        True
        >>> enviroment.run_server()
        True
        >>> os.system('python enviroment.py prueba clean') and True
        True
        '''
        try:
            if self.database:
                os.system('python %s/openerp-server -i base '
                          '-d %s -c %s/%s_config_file '
                          '--without-demo=True &' % \
                                                         (self.server_path,
                                                          self.database,
                                                          self.config_folder,
                                                          self.name.lower()))
            else:
                os.system('python %s/openerp-eerver -c %s/%s_config_file &' % \
                                                          (self.server_path,
                                                           self.config_folder,
                                                           self.name.lower()))
            return True
        except Exception, error:
            return error

        return False

if __name__ == "__main__":
    ARGS = sys.argv
    if 'create_postgres_user' in ARGS and len(ARGS) == 5:
        ENV = ServerEnviroment(ARGS[2], ARGS[3], ARGS[4], '', 'tmp', 'server')
        ENV.create_postgres_user()
    elif ARGS and len(ARGS) > 2 and ARGS[2] == 'clean':
        import subprocess
        os.system("userdel gerrard -rf")
        os.popen('python enviroment.py create_postgres_user postgres '
                 'liverpool thecaptain') and True
        os.system("killall python")
    else:
        import doctest
        doctest.testmod()
