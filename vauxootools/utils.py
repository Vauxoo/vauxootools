import shutil
import pwd
import grp
import os
from glob import glob
import psycopg2
import subprocess


def chown_r(path, uid=-1, gid=-1):
    for item in glob(path+'/*'):
        if os.path.isdir(item):
            chown_r(os.path.join(path, item), uid, gid)
        else:
            try:
                os.chown(os.path.join(path, item), uid, gid)
            except:
                print('File permissions on {0} not updated due to error.'.format(os.path.join(path,item)))

def copy_instance(config):
    dest = os.path.join(config.get('working_dir'), config.get('instance_name'))
    try:
        shutil.copytree(config.get('instance'), dest)
    except:
        print('No se pudo copiar la instancia . '.config.get('instance'))        
    if config.get('user', False):
        uid = pwd.getpwnam(config.get('user')).pw_uid
        gid = grp.getgrnam(config.get('group', config.get('user'))).gr_gid
        chown_r(dest, uid, gid)

def create(config):
    try:
        conn = psycopg2.connect("host=%s dbname=postgres password=%s user=%s port=%s"%
                (config.get('db_host', 'localhost'), config.get('db_password'),config.get('db_user'), 
                    config.get('db_port', 5432)))
    except:
        print 'No se pudo conectar a la base de datos'

    try:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE %s ENCODING 'UTF8' TEMPLATE template1"%(config.get('db_name')))
    except Exception as e:
        print 'No se pudo crear la base de datos: ', e.message
    cur.close()
    conn.close()

def drop(config):
    try:
        conn = psycopg2.connect("host=%s dbname=postgres password=%s user=%s port=%s"%
                (config.get('db_host', 'localhost'), config.get('db_password'),config.get('db_user'), 
                    config.get('db_port', 5432)))
    except:
        print 'No se pudo conectar a la base de datos'

    try:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute("DROP DATABASE %s"%(config.get('db_name')))
    except Exception as e:
        print 'No se pudo borrar la base de datos: ', e.message

def backup(config):
    cmd = 'pg_dump -O -U %s %s -f %s -W -p %s' % 
            (config.get('db_user'), config.get('db_name'), config.get('file_name'),config.get('db_port'))
    subprocess.call(cmd, shell=True)
    # child = pexpect.spawn('pg_dump -O -U %s %s -f %s -W -p %s'%
    #             (connection['user'], database, destiny_file, connection['db.server']['port']))
    # child.expect('.*(P|p)assword:*')
    # child.sendline(connection['password'])
    # child.expect(pexpect.EOF)
