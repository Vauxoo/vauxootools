#! /usr/bin/env python
import oerplib
import getpass

class Instance(object):
    '''
     Return an Instance obj for that you can take the control about OERP lib
     objects and show logger obj with process error
     >>> import oerplib
     >>> con = oerplib.OERP('localhost', protocol='netrpc', port=8070)
    '''

    def __init__(self, **kwargs):
        self.dbname = kwargs.get('dbname')
        self.hostname = kwargs.get('hostname')
        self.password = kwargs.get('passwd', False) or getpass.getpass(
            'Insert the password for user %s: ' % kwargs.get('username'))
        self.port = kwargs.get('port')
        self.username = kwargs.get('username')
        self.logger = kwargs.get('logger')

    def server_login(self, **kwargs):
        '''
        Create an oerplib obejct logged with logged with parameters obtained
        for this methos
        @param host: String with the server location
        @param user: String with the user login
        @param password: String with the password for the sent user
        @param database: String with database name to get or set new records
        @param port: Integer with port to which the server works
        >>> user = con.login('admin', 'admin', database='db_name')
        >>> user.name
        u'Administrator'

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
        @param con: Oerplib object with server conection
        @param admin_pass: String with te super admin password to create
        database
        @param db_name: String with name to the new database

        >>> con.db.create_and_wait('1234', 'test_db', 'testp')
        [{'login': u'admin', 'password': u'testp'}]

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
        @param leads: List with possible lead ids
        @param server: Oerplib object with server to check if the lead exist
        @param model: String with _name module to check ids

        >>> con.execute('res.users', 'exists', 1)
        [1]

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
        @param server: Oerplib object of cfdi instance
        @param modules: List with modules name that will be install

        >>> ids = con.search('ir.module.module', [('name', '=', module)])
        >>> ids and con.execute('ir.module.module', 'button_immediate_install',
        ...                     ids)

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
