class DBBroker:
    def __init__(self, db) -> None:
        self.db = db

    def get(self, id, cls):
        table = self.db.table(str(cls))
        di = table.get(doc_id=id)
        di.update({"id": di.doc_id})
        obj = cls(**di)
        return obj

    def get_all(self, cls):
        table = self.db.table(str(cls))
        result = []
        for d in table.all():
            di = dict(d)
            di.update({"id": d.doc_id})
            obj = cls(**di)
            result.append(obj)
        return result

    def add(self, entity, cls):
        table = self.db.table(str(cls))
        return table.insert(entity.toJSON())

    def update(self, entity, id, cls):
        table = self.db.table(str(cls))
        table.update(entity.toJSON(), doc_ids=[id])
