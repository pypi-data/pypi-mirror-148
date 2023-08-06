import xmlrpc.client

from typing import List

class api:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.url = host
        self.db = database
        self.user = user
        self.password = password
        self.server = self.client()
        self.read = self.read_client()
        self.uid = self.authenticate()

    def client(self):
        return xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))

    def version(self):
        return self.server.version()

    def authenticate(self):
        return self.server.authenticate(self.db, self.user, self.password, {})

    def read_client(self):
        return xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

    def check_access(
            self,
            model: str,
            right: str = 'check_access_rights',
            chmod: List[str] = ['read'],
            raise_exception: bool = True,
    ):
        return self.read.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            right,
            chmod,
            {
                'raise_exception': raise_exception
            }
        )

    def search(self, model: str, condition: List[List[list]] = [[]], limit: int = -1, offset: int = -1):
        doc = {}
        if limit > 0:
            doc.update({'limit': limit})

        if offset > 0:
            doc.update({'offset': offset})

        return self.read.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            'search',
            condition,
            doc
        )

    def records(self, model: str, fields: List[str] = [], condition: List[List[list]] = [[]], limit: int = -1,
                offset: int = -1):
        ids = self.search(model, condition, limit, offset)
        return self.read.execute_kw(self.db, self.uid, self.password, model, 'read', [ids], {'fields': fields})

    def count_records(self, model: str, condition: List[List[list]] = [[]]):
        return self.read.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            'search_count',
            condition
        )

    def fields_get(self, model: str, condition: List[List[list]] = [[]], attributes: List[str] = []):
        return self.read.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            'fields_get',
            condition,
            {'attributes': attributes}
        )

    def search_read(self, model: str, condition: List[List[list]] = [[]], fields: List[str] = [], limit: int = -1,
                    offset: int = -1):
        filter = {'fields': fields}

        if limit > 0:
            filter.update({'limit': limit})

        if offset > 0:
            filter.update({'limit': offset})

        return self.read.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            'search_read',
            condition,
            filter
        )

    def create(self, model: str, data: list = []):
        return self.read.execute_kw(self.db, self.uid, self.password, model, 'create', data)

    def update(self, model: str, id: List[int], value: dict):
        return self.read.execute_kw(self.db, self.uid, self.password, model, 'write', [id, value])

    def delete(self, model: str, condtion: List[List[list]] = [[]]):
        return self.read.execute_kw(self.db, self.uid, self.password, model, 'unlink', condtion)
