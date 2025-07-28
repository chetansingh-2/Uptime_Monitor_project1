# monitor/tasks.py

from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task(name="run_custom_management_command")
def run_custom_command_task():
    try:
        logger.info("Executing custom management command...")
        call_command('check_sites')
        logger.info("Custom management command finished successfully.")
    except Exception as e:
        logger.error(f"Error executing management command: {e}")
