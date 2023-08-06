class Settings:
    """
        - Settings to use Celery and Redis
        - Define backend and broker url in celery
    """

    def __init__(self, **kwargs):
        self.backend = 'redis://localhost/0'
        self.broker  = 'redis://localhost/0'
        self.crontab = kwargs.get('crontab')

    def get_settings(self):

        print(f'\n***** Current Backend ==> {self.backend}')
        print(f'***** Current Broker ==> {self.broker}')

        if self.crontab:
            return

        print('\nIf inputs not provided, we will use the defaults ones\n')

        backend_input = input('Please your celery backend string:    ')
        broker_input  = input('Please your celery broker string:    ')

        if backend_input:
            self.backend = backend_input

        if broker_input:
            self.broker = broker_input

        return
