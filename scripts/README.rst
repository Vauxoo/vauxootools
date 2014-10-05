Command Reference
=================

When you install this package some cli will be availables for you, all this
tools/commands will be listed in this section of the documentation.

Configuration files.
--------------------

All configuration files respect the xdg way to do things, it means you can run
your script reading automagically your config files from global enviroment,
overwrite the user enviroment or even run from local.cfg file.::

    /etc/xdg/<script_name>/<script_name>.cfg
    /home/<user>/.config/<script_name>/<script_name>.cfg
    ./local.cfg

Then said this, for all command explained below you will need to do this steps.

    1. Run the --help to know the options availables for this command.
    2. Create a config file in some of paths explained above with this format::
    
           [__main__]
           key=value

    3. Run your script and enjoy it.
    4. As they are scripts which are mainly used to repetitive jobs remember
       you have the cron_ from linux in your hand.
    

Script Name: simpletimetracker.
-------------------------------


Script Name: openerp_verify.
----------------------------

Simple script to sniff if a server is running or not, based on vauxootools and
oerplib it only ask for dblist to ensure openerp is up.

Run to know all options::

    $openerp_verify --help

To test the script with your server::

    $openerp_verify -H ip.of.your.server -P PORTNUMBER

Example::

    $openerp_verify -H erp.example.com -P 8069

You can save the logfile in an specific path to analize later.::

    $openerp_verify -H erp.example.com -P 8069 -l /var/log/openerp_verify.log

.. _cron: http://www.ibm.com/developerworks/opensource/library/l-job-scheduling/index.html
