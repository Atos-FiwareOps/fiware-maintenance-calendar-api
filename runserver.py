from maintenance_calendar import app
import maintenance_calendar.views
from maintenance_calendar import config

#inicalize the Logger of Flask
from flask_log import Logging
import logging
root_logger = logging.getLogger()

#configure rotatin handler
file_hander = logging.handlers.RotatingFileHandler(config.log_file, maxBytes=config.maxbytes_log_file, backupCount=config.backupCount_log_file)
root_logger.addHandler(file_hander)
#configure console handler
console_logger = logging.StreamHandler()
root_logger.addHandler(console_logger)
app.config['FLASK_LOG_LEVEL'] = config.log_level
flask_log = Logging(app)
flask_log.set_formatter(config.formatter_log)

try:
	app.run(host='0.0.0.0', port=8085, debug=True)

finally:
	logging.info("Closing the handers of the logging")
	root_logger.removeHandler(file_hander)
	file_hander.close()
	root_logger.removeHandler(console_logger)
	console_logger.close()