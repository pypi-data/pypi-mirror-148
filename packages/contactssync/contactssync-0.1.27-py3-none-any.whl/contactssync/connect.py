from abc import ABC, abstractmethod
import collections

class Connection:

    @classmethod
    @abstractmethod
    def contact_type(cls):
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def dict_to_contact(cls, d):
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def contact_to_dict(cls, c, **kwargs):
        return NotImplementedError()

    def _convert_to_contact_and_drop_none(self, ds):
        def _dict_to_contact_and_store(ctx, d):
            c = ctx.dict_to_contact(d)
            if c is None:
                return None
            c._source_dict = d
            return c

        if (not isinstance(ds, collections.Iterable) or
                isinstance(ds, collections.Mapping)):
            ds = [ds]
        clist = [_dict_to_contact_and_store(self, d) for d in ds]
        return [c for c in clist if c is not None]

    @abstractmethod
    def get(self, id, convert=True):
        raise NotImplementedError()

    @abstractmethod
    def get_by_name(self, fn, ln, convert=True):
        raise NotImplementedError()

    @abstractmethod
    def create(self, d):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, c):
        raise NotImplementedError()

    @abstractmethod
    def update(self, c):
        raise NotImplementedError()

    @abstractmethod
    def list(self):
        raise NotImplementedError()

    @abstractmethod
    def query(self, query_dict):
        raise NotImplementedError()

    @abstractmethod
    def create_batch(self, batch):
        raise NotImplementedError()

    @abstractmethod
    def update_batch(self, batch):
        raise NotImplementedError()
