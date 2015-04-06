__author__ = 'wfournier'
admin_email = 'dkars@fournier.nl'
postfix_virtual = '/etc/postfix/virtual.test'


import logging
import json
import sh
import os

logger = logging.getLogger('controller')
logging_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logging.json')
config = json.loads(open(logging_conf).read())
logging.config.dictConfig(config)


def update_mail_forwards(_):
    session.mail_forward_error = None
    with open(postfix_virtual, 'w+') as virtual:
        for record in db(db.t_mail_forwards).select():
            if record.f_enabled:
                if '@' not in record.f_call:
                    source = '{}@dkars.nl'.format(record.f_call)
                else:
                    source = record.f_call
                logger.debug('{} {}'.format(source, record.f_destination_address))
                virtual.write('{} {}\n'.format(source, record.f_destination_address))
    try:
        result = sh.sudo('postmap', '-p', postfix_virtual)
        logger.debug('Postmap returned: \n{}\n{}'.format(result.stdout, result.stderr))
    except Exception as e:
        logger.error('Postmap returned: {}'.format(e))
        session.mail_forward_error = str(e)
        mail.send(admin_email, 'Postmap failed', str(e))
        return False


