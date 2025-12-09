#!/usr/bin/env python3

from typing import Literal
import logging
from datetime import datetime

def format_log_output(message):
	now = datetime.now()
	formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
	message = str(message).replace("\n", f"\n{formatted_time} - ")
	output = f"{formatted_time} - {message}"
	
	return output

def log(message: str, log_level: Literal["debug", "info", "warning", "error", "critical"] = "info", console_output: bool = True) -> None:
	"""
	Logs events to both the console and a log file.

	Args:
		message (str): The message to be logged and printed to the console.
		log_level (str, optional): The severity level of the log. Defaults to "info".
		Possible values: "debug", "info", "warning", "error", "critical".
	"""
	
	output = format_log_output(message)
	
	if console_output:
		print(output)
	
	logging_levels = {
		"debug": logging.debug,
		"info": logging.info,
		"warning": logging.warning,
		"error": logging.error,
		"critical": logging.critical
	}
	
	logging_levels[log_level](output)
			
def log_exception(message: str) -> None:
		logging.exception(message)
	
# # Configure logging
# logging.basicConfig(
# 	filename="../docs/app.log",
# 	level=logging.DEBUG,  # Log level (DEBUG logs everything)
# 	format="%(asctime)s - %(levelname)s - %(message)s",
# 	datefmt="%m-%d-%Y %H:%M:%S",
# )


