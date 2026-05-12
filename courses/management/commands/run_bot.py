from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os
import logging

# Add the bot directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

class Command(BaseCommand):
    help = 'Run the Bale Messenger bot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            type=str,
            help='Bale bot token (overrides settings)',
        )

    def handle(self, *args, **options):
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        token = options.get('token') or getattr(settings, 'BOT_TOKEN', None)
        
        if not token:
            self.stdout.write(
                self.style.ERROR('BOT_TOKEN not found! Add it to settings.py or pass --token argument')
            )
            return
        
        self.stdout.write(self.style.SUCCESS(f'Starting Bale bot with token: {token[:10]}...'))
        
        try:
            # Import and run bot
            from bot.bale_bot import BaleCourseBot
            bot = BaleCourseBot()
            bot.run()
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'Failed to import bot module: {e}'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('\nBot stopped by user.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Bot error: {e}'))