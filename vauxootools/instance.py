#! /usr/bin/env python
import oerplib

class Instance(object):
    '''
     Return an Instance obj for that you can take the control about OERP lib
     objects and show logger obj with process error
     >>> from vauxootools import VauxooToolsServers
     >>> from instance import Instance
     >>> configuration = VauxooToolsServers(app_name='App Test',
     ...                  usage_message="Created by VauxooTools",
     ...                  options=['dbname', 'hostname', 'il', 'password',
     ...                           'port', 'sd', 'sh', 'spo', 'sp', 'su',
     ...                           'username'])

     configuration is a vauxootools object with all sent manage parameter

     >>> con = Instance(dbname='localhost', hostname='localhost',
     ...                port=8070, username='admin',
     ...                logger=configuration.logger)

     con is an oerplib wrapper to take control of traceback error
    '''

    def __init__(self, **kwargs):
        self.dbname = kwargs.get('dbname')
        self.hostname = kwargs.get('hostname')
        self.password = kwargs.get('passwd', 'admin')
        self.port = kwargs.get('port')
        self.username = kwargs.get('username')
        self.logger = kwargs.get('logger')

    def server_login(self, **kwargs):
        '''
        Create an oerplib obejct logged with logged with parameters obtained
        for this methos

         >>> from vauxootools import VauxooToolsServers
         >>> from instance import Instance
         >>> configuration = VauxooToolsServers(app_name='App Test',
         ...                  usage_message="Created by VauxooTools",
         ...                  options=['dbname', 'hostname', 'il', 'password',
         ...                           'port', 'sd', 'sh', 'spo', 'sp', 'su',
         ...                           'username'])

         configuration is a vauxootools object with all sent manage parameter

         >>> con = Instance(dbname='localhost', hostname='localhost',
         ...                port=8070, username='admin',
         ...                logger=configuration.logger)

         >>> login = con.server_login(host='localhost', user='admin',
         ...                          password='admin',
         ...                          database='test_db', port=8070)

        @param host: String with the server location
        @param user: String with the user login
        @param password: String with the password for the sent user
        @param database: String with database name to get or set new records
        @param port: Integer with port to which the server works


        :raise: :class:`oerplib.error.RPCError`
        :return: a oerplib login object or False if any parameter is wrong
        '''

        con = oerplib.OERP(
            server=kwargs.get('host'),
            database=kwargs.get('database'),
            port=int(kwargs.get('port')),
        )
        try:
            con.login(kwargs.get('user'), kwargs.get('password'))
            self.logger.info("Logged with user %s" % (kwargs.get('user')))
        except Exception, error:
            con = False
            self.logger.error("We can't do login in the iserver: "
                              "http://%s:%s with user %s" % \
                                      (kwargs.get('host'), kwargs.get('port'),
                                      kwargs.get('user')))
            self.logger.error(error)
        return con

    def create_database(self, con, admin_pass, db_name):
        '''
        Creates a new databae to install modules for create a cfdi_instance

         >>> from vauxootools import VauxooToolsServers
         >>> from instance import Instance
         >>> configuration = VauxooToolsServers(app_name='App Test',
         ...                  usage_message="Created by VauxooTools",
         ...                  options=['dbname', 'hostname', 'il', 'password',
         ...                           'port', 'sd', 'sh', 'spo', 'sp', 'su',
         ...                           'username'])

         configuration is a vauxootools object with all sent manage parameter

         >>> con = Instance(dbname='localhost', hostname='localhost',
         ...                port=8070, username='admin',
         ...                logger=configuration.logger)

         >>> login = con.server_login(host='localhost', user='admin',
         ...                          password='admin',
         ...                          database='test_db', port=8070)
         >>> db = con.create_database(login, 'admin', '1234')

        @param con: Oerplib object with server conection
        @param admin_pass: String with te super admin password to create
        database
        @param db_name: String with name to the new database

        :return: False o a dict with login information
        :raise: :class:`oerplib.error.RPCError`
        '''
        login = False
        try:
            if not db_name in con.db.list():
                self.logger.info("Creating db %s" % db_name)
                login = con.db.create_and_wait(
                    admin_pass, db_name, admin_passwd='1234')
            else:
                self.logger.error("We can't create the database %s because "
                        "there is a database with the same name" % db_name)

        except Exception, error:
            self.logger.error("We can't create the database %s" % db_name)
            self.logger.error(error)

        return login

    def check_ids(self, ids, server, model='crm.lead'):
        '''
        Verifies the lead ids to be sure than all are valid ids


         >>> from vauxootools import VauxooToolsServers
         >>> from instance import Instance
         >>> configuration = VauxooToolsServers(app_name='App Test',
         ...                  usage_message="Created by VauxooTools",
         ...                  options=['dbname', 'hostname', 'il', 'password',
         ...                           'port', 'sd', 'sh', 'spo', 'sp', 'su',
         ...                           'username'])

         configuration is a vauxootools object with all sent manage parameter

         >>> con = Instance(dbname='localhost', hostname='localhost',
         ...                port=8070, username='admin',
         ...                logger=configuration.logger)

         >>> login = con.server_login(host=con.hostname, user='admin',
         ...                          password='admin',
         ...                          database='test_db', port=con.port)
         >>> for i in  con.check_ids([1], login, 'res.users'):
         ...     print i
         1

        @param leads: List with possible lead ids
        @param server: Oerplib object with server to check if the lead exist
        @param model: String with _name module to check ids


        :return: List with existing ids
        :raise: :class:`oerplib.error.RPCError`
        '''
        for i in ids:
            if str(i).isdigit():
                if server.execute(model, 'exists', int(i)):
                    yield(int(i))
                else:
                    self.logger.error("The record with id %s don't exist" % i)

    def install_modules(self, server, modules):
        '''
        Install modules sent


         >>> from vauxootools import VauxooToolsServers
         >>> from instance import Instance
         >>> configuration = VauxooToolsServers(app_name='App Test',
         ...                  usage_message="Created by VauxooTools",
         ...                  options=['dbname', 'hostname', 'il', 'password',
         ...                           'port', 'sd', 'sh', 'spo', 'sp', 'su',
         ...                           'username'])

         configuration is a vauxootools object with all sent manage parameter

         >>> con = Instance(dbname='localhost', hostname='localhost',
         ...                port=8070, username='admin',
         ...                logger=configuration.logger)

         >>> login = con.server_login(host=con.hostname, user='admin',
         ...                          password='admin',
         ...                          database='test_db', port=con.port)
         >>> con.install_modules(login, ['account'])

        @param server: Oerplib object of cfdi instance
        @param modules: List with modules name that will be install


        :raise: :class:`oerplib.error.RPCError`
        '''
        for module in modules:
            ids = server.search('ir.module.module', [('name', '=', module)])
            if ids:
                self.logger.info("Installing module %s" % module)
                server.execute('ir.module.module',
                               'button_immediate_install', ids)
            else:
                self.logger.warnning("The module %s is not avaliable in the "
                                     "server" % module)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
