from __future__ import annotations

import uuid
import io
import datetime
from drb import DrbNode
from drb.path import ParsedPath
from drb.predicat import Predicate
from drb.exceptions import DrbException
from requests.auth import AuthBase
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from .odata_node import OdataNode
from .odata_utils import req_svc_products, req_product_by_uuid, \
    req_svc_count, req_product_download, req_product_attributes,\
    ODataQueryPredicate, OdataServiceType, get_type_odata_svc
from .exceptions import OdataRequestException


class ODataServiceNode(OdataNode):
    def __init__(self, url: str, auth: AuthBase = None):
        super(ODataServiceNode, self).__init__(url, auth)
        self.__path = ParsedPath(url)
        self._type = None

    @property
    def type_service(self) -> OdataServiceType:
        if self._type is None:
            self._type = get_type_odata_svc(self._service_url, self._auth)
        return self._type

    @property
    def name(self) -> str:
        return self._service_url

    @property
    def namespace_uri(self) -> Optional[str]:
        if self.type_service == OdataServiceType.DHUS:
            return 'OData.DHuS'
        elif self.type_service == OdataServiceType.ONDA_DIAS:
            return 'Ens'
        else:
            return 'OData.CSC'

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def children(self) -> List[DrbNode]:
        return ODataFilteredList(self)

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException('ODataNode has no attribute')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return len(req_svc_products(
                    self, filter=f"Name eq '{name}'")) > 0
            return req_svc_count(self) > 0
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f"ODataNot doesn't support {impl} implementation")

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) \
            -> Union[DrbNode, List[DrbNode]]:
        if self.type_service == OdataServiceType.ONDA_DIAS:
            id_identifier = 'id'
        else:
            id_identifier = 'Id'

        if namespace_uri is None:
            if self.type_service == OdataServiceType.ONDA_DIAS:
                products = req_svc_products(self, search=f'"{name}"')
            else:
                products = req_svc_products(self, filter=f"Name eq '{name}'")
            if len(products) <= 0:
                raise DrbException(f'No child ({name}, {namespace_uri},'
                                   f' {occurrence}) found')
            p = products[occurrence]
            if isinstance(p, list):
                return [ODataProductNode(self,
                                         x[id_identifier], data=x) for x in p]
            return ODataProductNode(self, p[id_identifier], data=p)
        raise DrbException(f'No child ({name}, {namespace_uri}, {occurrence}) '
                           'found')

    def __retrieve_child_from_tuple(self, t: tuple) -> \
            Union[List[DrbNode], DrbNode]:
        if len(t) == 2:
            # (name, namespace)
            if t[1] is None or isinstance(t[1], str):
                return self._get_named_child(name=t[0], namespace_uri=t[1])
            # (name, occurrence)
            elif isinstance(t[1], int) or isinstance(t[1], slice):
                return self._get_named_child(t[0], occurrence=t[1])
        # (name, namespace, occurrence)
        elif len(t) == 3:
            return self._get_named_child(*t)
        raise KeyError(f'Invalid key: {t}')

    def __retrieve_child(self, key: Union[uuid.UUID, tuple, Predicate]) -> \
            Union[List[DrbNode], DrbNode]:
        if self.type_service == OdataServiceType.ONDA_DIAS:
            id_identifier = 'id'
        else:
            id_identifier = 'Id'
        try:
            if isinstance(key, uuid.UUID):
                prd_uuid = str(key)
                data = req_product_by_uuid(self, prd_uuid)
                return ODataProductNode(self, str(prd_uuid), data=data)
            if isinstance(key, tuple):
                return self.__retrieve_child_from_tuple(key)
            if isinstance(key, str):
                return self._get_named_child(key)
            if isinstance(key, ODataQueryPredicate):
                return ODataFilteredList(self, key.filter, key.order)
        except DrbException as ex:
            raise KeyError from ex
        raise TypeError('Invalid type for a DrbNode bracket: '
                        f'{key.__class__}')

    def __len__(self):
        return req_svc_count(self)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.children[item]
        return self.__retrieve_child(item)

    def __truediv__(self, other):
        return self.__retrieve_child(other)


class ODataFilteredList(list):
    _page_size = 100

    def __init__(self, odata: OdataNode, qfilter: str = None,
                 qorder: str = None):
        super().__init__()
        self._count = -1
        self._page = None
        self._skip = 0
        self._odata = odata
        default = self.__retrieve_default_criteria(odata)
        self._filter = self.__prepare_filter(qfilter, default)
        self._order = self.__prepare_order(qorder, default)

    @classmethod
    def __retrieve_default_criteria(cls, odata: OdataNode) -> str:
        if odata.type_service == OdataServiceType.DHUS:
            return 'CreationDate'
        elif odata.type_service == OdataServiceType.ONDA_DIAS:
            return 'creationDate'
        elif odata.type_service == OdataServiceType.CSC:
            return 'PublicationDate'
        else:
            raise DrbException('Unsupported OData service')

    @classmethod
    def __prepare_filter(cls, user_filter: str, default: str) -> str:
        date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        if user_filter is None:
            return f'{default} lt {date}'
        if default in user_filter:
            return user_filter
        return f"({user_filter}) and {default} lt {date}"

    @classmethod
    def __prepare_order(cls, user_order: str, default: str) -> str:
        if user_order is None:
            return f'{default} desc'
        return user_order

    def __generate_product(self, data: dict) -> ODataProductNode:
        if self._odata.type_service == OdataServiceType.ONDA_DIAS:
            return ODataProductNode(self._odata, data['id'], data=data)
        else:
            return ODataProductNode(self._odata, data['Id'], data=data)

    def __perform_query(self):
        if self._count == -1:
            buffer, self._count = req_svc_products(self._odata, count=True,
                                                   filter=self._filter,
                                                   order=self._order,
                                                   skip=self._skip,
                                                   top=self._page_size)
        else:
            buffer = req_svc_products(self._odata, filter=self._filter,
                                      order=self._order, skip=self._skip,
                                      top=self._page_size)
        self._page = [self.__generate_product(e) for e in buffer]

    def __compute_index(self, item: Union[int, slice]) -> Tuple[int, int]:
        if isinstance(item, int):
            if item < 0:
                return item + len(self), -1
            return item, -1
        # item is a slice
        start = item.start if item.start is not None else 0
        if start < 0:
            start = start + len(self)
        stop = item.stop if item.stop is not None else len(self)
        if stop < 0:
            stop = stop + len(self)
        return start, stop

    def append(self, obj: Any) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def copy(self) -> List[ODataProductNode]:
        raise NotImplementedError

    def count(self, value: Any) -> int:
        raise NotImplementedError

    def extend(self, iterable: Iterable[ODataProductNode]) -> None:
        raise NotImplementedError

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        raise NotImplementedError

    def insert(self, index: int, obj: ODataProductNode) -> None:
        raise NotImplementedError

    def pop(self, index: int = ...) -> ODataProductNode:
        raise NotImplementedError

    def remove(self, value: Any) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def sort(self: List, *, key: None = ..., reverse: bool = ...) -> None:
        raise NotImplementedError

    def __getitem__(self, item):
        if self._count == -1:
            self.__perform_query()

        if isinstance(item, int):
            index, _ = self.__compute_index(item)
            if index not in range(self._skip, self._skip + self._page_size):
                page_number = index // self._page_size
                self._skip = page_number * self._page_size
                self.__perform_query()
            return self._page[index % self._page_size]
        elif isinstance(item, slice):
            start, stop = self.__compute_index(item)
            result = []
            total = stop - start
            page = 0
            while len(result) < total:
                skip = (page * self._page_size) + start
                top = min(total - len(result), self._page_size)
                resp = req_svc_products(self._odata, filter=self._filter,
                                        order=self._order, skip=skip, top=top)
                result.extend(resp)
                page += 1
            return [self.__generate_product(e) for e in result]
        else:
            raise KeyError(f'Invalid key: {type(item)}')

    def __iter__(self):
        def generator(qfilter, qorder, count, page_size):
            page_num = 0
            buffer = None
            for i in range(count):
                if i % page_size == 0:
                    skip = page_size * page_num
                    buffer = req_svc_products(self._odata, filter=qfilter,
                                              order=qorder, skip=skip,
                                              top=page_size)
                    page_num += 1
                idx = i % page_size
                yield self.__generate_product(buffer[idx])
        return generator(self._filter, self._order, len(self), self._page_size)

    def __len__(self):
        if self._count == -1:
            self.__perform_query()
        return self._count

    def __contains__(self, item):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __imul__(self, other):
        raise NotImplementedError


class ProductList(list):
    """
    Specific read only list to access to OData CSC Product entities:
     * Any access generate a remote access to the associated OData service
     * Any inherited functions allowing to modify the list have no effect.
     * comparator functions are not supported except the equal comparator.
    """

    def __init__(self, odata: ODataServiceNode):
        super().__init__()
        self.__odata = odata
        if self.__odata.type_service == OdataServiceType.ONDA_DIAS:
            self.__id_identifier = 'id'
        else:
            self.__id_identifier = 'Id'

    def __getitem__(self, item):
        count = req_svc_count(self.__odata)
        if isinstance(item, int):
            if -count < item >= count:
                raise IndexError
            if item >= 0:
                skip = item
            else:
                skip = item + count
            products = req_svc_products(self.__odata, skip=skip, top=1)
            prd = products[0]
            prd_uuid = products[0][self.__id_identifier]
            return ODataProductNode(self.__odata, prd_uuid, data=prd)
        if isinstance(item, slice):
            products = req_svc_products(self.__odata, skip=item.start,
                                        top=item.stop)
            return [ODataProductNode(self.__odata, p[self.__id_identifier],
                                     data=p)
                    for p in products]
        raise TypeError

    def __iter__(self):
        def iterator():
            for index in range(0, len(self)):
                p = req_svc_products(self.__odata, skip=index, top=1)
                yield ODataProductNode(self.__odata,
                                       p[0][self.__id_identifier], data=p[0])

        return iterator()

    def __len__(self):
        return req_svc_count(self.__odata)

    def __sizeof__(self):
        super().__sizeof__()

    def append(self, obj: Any) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def copy(self) -> List[ODataProductNode]:
        raise NotImplementedError

    def count(self, value: Any) -> int:
        raise NotImplementedError

    def extend(self, iterable: Iterable[ODataProductNode]) -> None:
        raise NotImplementedError

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        raise NotImplementedError

    def insert(self, index: int, obj: ODataProductNode) -> None:
        raise NotImplementedError

    def pop(self, index: int = ...) -> ODataProductNode:
        raise NotImplementedError

    def remove(self, value: Any) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def sort(self: List, *, key: None = ..., reverse: bool = ...) -> None:
        raise NotImplementedError


class ODataProductNode(OdataNode):
    def __init__(self, source: Union[str, OdataNode],
                 product_uuid: str = None,
                 data: Dict = None,
                 **kwargs):
        self._type = OdataServiceType.UNKNOWN

        if isinstance(source, OdataNode):
            super(ODataProductNode, self).__init__(source.get_service_url(),
                                                   source.get_auth())
            self._type = source.type_service
            self.__parent = source
            self.__uuid = product_uuid
        elif isinstance(data, Dict):
            self.__parent = None
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super(ODataProductNode, self).__init__(
                source.split('/Products')[0],
                auth
            )
            self._type = get_type_odata_svc(source.split('/Products')[0], auth)
            self.__uuid = data.get('id') if \
                self._type == OdataServiceType.ONDA_DIAS.value \
                else data.get('Id')
        else:
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super(ODataProductNode, self).__init__(
                source.split('/Products')[0],
                auth
            )
            self.__parent = None
            self.__uuid = product_uuid

        self.__path = ParsedPath(
            f'{self.get_service_url()}/Products({self.__uuid})')
        self.__product = kwargs.get('data', None)
        self.__attr = None

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    def __load_product(self):
        if self.__product is None:
            self.__product = req_product_by_uuid(self, self.__uuid)

    @property
    def name(self) -> str:
        self.__load_product()
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__product['name']
        else:
            return self.__product['Name']

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        self.__load_product()
        return {(k, None): v for k, v in self.__product.items()}

    @property
    def children(self) -> List[DrbNode]:
        return [ODataProductAttributeNode(self, self.__uuid)]

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        self.__load_product()
        if namespace_uri is None:
            try:
                return self.__product[name]
            except KeyError:
                pass
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name == self.children[0].name
            return True
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        if self.type_service == OdataServiceType.ONDA_DIAS:
            online = not self.get_attribute('offline')
        else:
            online = self.get_attribute('Online')
        return online and (impl == io.BufferedIOBase or impl == io.BytesIO)

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            return req_product_download(self,
                                        self.__uuid,
                                        kwargs.get('start', None),
                                        kwargs.get('end', None)
                                        )
        raise DrbException(f'Not supported implementation: {impl}')

    def __eq__(self, other):
        if isinstance(other, ODataProductNode):
            return super().__eq__(other) and other.__uuid == self.__uuid
        return False

    def __hash__(self):
        return hash(self._service_url)


class ODataProductAttributeNode(OdataNode):
    __name = 'Attributes'

    def __init__(self, source: ODataProductNode, prd_uuid: str):
        super().__init__(source.get_service_url(), source.get_auth())
        self.__uuid = prd_uuid
        self.__parent = source
        self.__attr = None
        self._type = source.type_service

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    def __load_attributes(self) -> None:
        if self.__attr is None:
            self.__attr = req_product_attributes(self, self.__uuid)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__parent.path / self.__name

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def children(self) -> List[DrbNode]:
        self.__load_attributes()
        return [ODataAttributeNode(self, data=x) for x in self.__attr]

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                for x in self.__attr:
                    if name in x.keys():
                        return True
                return False
            return len(self.__attr) > 0
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f'Do not support implementation: {impl}')


class ODataAttributeNode(OdataNode):
    def __init__(self, source: Union[str, ODataProductAttributeNode],
                 **kwargs):
        if isinstance(source, ODataProductAttributeNode):
            super().__init__(source.get_service_url(), source.get_auth())
            self.__parent = source
            self._type = source.type_service
        elif isinstance(source, str):
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super().__init__(source, auth)
            self.__parent = None
            self._type = OdataServiceType.UNKNOWN
        else:
            raise OdataRequestException(f'Unsupported source: {type(source)}')
        self.__path = None
        self.__data = kwargs['data'] if 'data' in kwargs.keys() else None

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    @property
    def name(self) -> str:
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__data['name']
        else:
            return self.__data['Name']

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__data['value']
        else:
            return self.__data['Value']

    @property
    def path(self) -> ParsedPath:
        if self.__path is None:
            if self.__parent is None:
                self.__path = ParsedPath(self.name)
            else:
                self.__path = self.__parent.path / self.name
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {(k, None): v for k, v in self.__data.items()}

    @property
    def children(self) -> List[DrbNode]:
        return []

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None and name in self.__data.keys():
            return self.__data[name]
        raise DrbException(f'Attribute not found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f'Do not support implementation: {impl}')
