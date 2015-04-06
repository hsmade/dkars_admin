__author__ = 'wfournier'
admin_email = 'dkars@fournier.nl'
postfix_virtual = '/etc/postfix/virtual'


import logging
import json
logger = logging.getLogger('controller')
config = json.loads(open('logging.json').read())
logging.config.dictConfig(config)
import sh


def update_mail_forwards(_):
    global error
    with open(postfix_virtual, 'w+') as virtual:
        for record in db(db.t_mail_forwards).select():
            if '@' not in record.f_call:
                source = '{}@dkars.nmessage_textl'.format(record.f_call)
            else:
                source = record.f_call
            logger.info('{}\t{}'.format(source, record.f_destination_address))
            virtual.write('{}\t{}'.format(source, record.f_destination_address))
    try:
        sh.sudo('postmap', postfix_virtual)
    except Exception as e:
        logger.error('Postmap returned: {}'.format(e))
        logger.debug('error before:{}'.format(error))
        error = str(e)
        logger.debug('error after:{}'.format(error))
        # response.flash('Postmap error: {}'.format(e))
        mail.send(admin_email, 'Postmap failed', str(e))
        return False


