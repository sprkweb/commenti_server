import os

# Commenti settings
COMMENTI_ALLOW_DELETE = os.environ.get('COMMENTI_ALLOW_DELETE', 'true').lower() == 'true'
COMMENTI_ALLOW_EDIT = os.environ.get('COMMENTI_ALLOW_EDIT', 'true').lower() == 'true'
