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
        '''
        Class's Builder to set the main values and use them in all methods for
        this class. When you instance the 'Instance' Class you must set each
        variable in the instance declaration

        Variable that must get this Class:

        dbname = String with name of the database to use
        hostname = String with  OpenERP server location
        port = String with port which OpenERP works
        username = String user name to do login in OpenERP
        passwd = String with passwd of user to do login
        logger = Logger obj to show error, warning and info messages

        from instance import Instance
        instance_obj = Instance(dbname='localhost', hostname='localhost',
                                port=8070, username='admin', passwd='admin',
                                logger=loggeri_obj)
        '''
        self.dbname = kwargs.get('dbname')
        self.hostname = kwargs.get('hostname')
        self.password = kwargs.get('passwd', 'admin')
        self.sadminpwd = kwargs.get('sadminpwd', 'admin')
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
            timeout=999999999999999,
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
                    self.logger.error("The record id %s in the model "
                                      "%s don't exist" % (i, model))

    def get_model_fields(self, ids, server, model='crm.lead', field='all'):
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
         >>> con.get_model_fields(1, login, 'res.users', 'name')
         Administrator

        @param ids: Integer with record id
        @param server: Oerplib object with server to check if the lead exist
        @param model: String with _name module to check ids
        @param field: String with name field all by default


        :return: Value of field or False is the field don't exist
        :raise: :class:`oerplib.error.RPCError`
        '''
        fields = field == 'all' and [] or type(field) == list and field or \
                 [field]
        record = server.read(model, ids, fields)
        if  field == 'all' and [] or type(field) == list:
            return record
        else:
            return record.get(field, False)

        return True

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
                self.logger.warning("The module %s is not avaliable in the "
                                     "server" % module)
    def upgrade_modules(self, server, modules):
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
         >>> con.upgrade_modules(login, ['account'])

        @param server: Oerplib object of cfdi instance
        @param modules: List with modules name that will be install


        :raise: :class:`oerplib.error.RPCError`
        '''
        for module in modules:
            ids = server.search('ir.module.module', [('name', '=', module)])
            if ids:
                self.logger.info("Updating module %s" % module)
                server.execute('ir.module.module',
                               'button_immediate_upgrade', ids)
            else:
                self.logger.warning("The module %s is not avaliable in the "
                                     "server" % module)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
