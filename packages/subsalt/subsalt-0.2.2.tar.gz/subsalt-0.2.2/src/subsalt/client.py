import pandas, requests, typing, warnings, psycopg2

urls = {
    'Auth': 'https://api.getsubsalt.com/v1/token',
    'Fetch': 'https://api.getsubsalt.com/v1/datasets'
}

class TableMetadata(object):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table

class Client(object):
    API_MODE = 1
    DB_MODE = 2

    def __init__(self, client_id=None, client_secret=None, username=None, password=None):
        self.mode = None

        if client_id and client_secret:
            self.mode = Client.API_MODE

            self.client_id = client_id
            self.client_secret = client_secret

            self.access_token = None

            warnings.warn('Subsalt running in legacy API mode; this will be deprecated in future versions. Please upgrade to DB mode.', DeprecationWarning, stacklevel=2)

        if username and password:
            self.mode = Client.DB_MODE

            self.username = username
            self.password = password

            self.conn = None

        if self.mode is None:
            raise Exception('Must provide either client_id and client_secret, or username and password')


    def _auth(self) -> None:
        resp = requests.post(urls['Auth'], {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

        if resp.ok:
            self.access_token = resp.json()['access_token']
        else:
            raise resp.raise_for_status()

    def _dbauth(self) -> None:
        self.conn = psycopg2.connect(
            host='connect.subsalt.io',
            dbname='subsalt',
            user=self.username,
            password=self.password,
        )

    def get(self, model_id: str, limit: int = 100) -> pandas.DataFrame:
        '''
        Retrieve `limit` records from the specified model, and return a dataframe. The default
        limit is 100 records.
        '''
        if self.mode == Client.DB_MODE:
            raise Exception('Client.get() only available in API mode')

        if self.access_token is None:
            self._auth()
        
        url = '{}/{}?limit={}'.format(urls['Fetch'], model_id, limit)
        resp = requests.get(url, headers={
            'Authorization': 'Bearer {}'.format(self.access_token)
        })

        if resp.ok:
            data = resp.json()['data']
            return pandas.DataFrame(data)
        else:
            raise resp.raise_for_status()

    def tables(self) -> typing.List[TableMetadata]:
        if self.mode == Client.API_MODE:
            raise Exception('Client.tables() only available in DB mode')
        
        if self.conn == None:
            self._dbauth()

        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT table_schema, table_name 
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ''')

        return [ TableMetadata(*table) for table in cursor.fetchall() ]
    
    def sql(self, sql):
        if self.mode == Client.API_MODE:
            raise Exception('Client.sql() only available in DB mode')

        if self.conn == None:
            self._dbauth()

        cursor = self.conn.cursor()
        cursor.execute(sql)

        return pandas.DataFrame(
            cursor.fetchall(),
            columns=[ desc[0] for desc in cursor.description ]
        )