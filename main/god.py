# -*- coding: utf-8 -*-
"""
config必须配置
OBJECT_ID_WIDTH = 10 ** 13
MYSQL = ('172.25.1.111', 3306, 'GoBelieve_user', 'GoBelieve_user.mysql', 'game_center', True, 'utf8')
"""
from flask import g
from functools import partial
import types
from utils.mysql import get_mysql
import time
import re
from utils.pager import Pager
from config import MYSQL
from contextlib import contextmanager


class Exp(object):
    """格式化sql的字段
    `field`=%s+%s => table.field=%s+%s
    `field1`+`a.field2`<>%s => table.field1+a.field2=%s
    """
    def __init__(self, pattern, *args):
        self._pattern = pattern
        self._fields = re.findall(r'`[^`]+`', self._pattern)
        self._values = args

    def format(self, obj):
        pattern = self._pattern
        for field in self._fields:
            field_strip = field.strip('`')
            replace = obj.escape_field(field_strip)
            pattern = pattern.replace(field, replace)

        return pattern, self._values


class Where(object):
    """格式化sql的where
    """
    _glue = None

    def __init__(self, *args):
        self.args = list(args)

    def append(self, item):
        self.args.append(item)

    def __len__(self):
        return len(self.args)

    def format(self, obj):
        items = []
        values = []
        for arg in self.args:
            if isinstance(arg, Exp):
                item, seq_values = arg.format(obj)
                items.append(item)
                values.extend(seq_values)
            elif isinstance(arg, str) and '.' not in arg:
                items.append("{}=%s".format(obj.escape_field(arg)))
                values.append(obj.get(arg))
            elif isinstance(arg, Where):
                sub_items, sub_values = arg.format(obj)
                items.append(sub_items)
                values.extend(sub_values)

        if items:
            return "({})".format(self._glue.join(items)), values
        else:
            return "", values


class And(Where):
    _glue = ' AND '


class Or(Where):
    _glue = ' OR '


def unique_id(obj_type):
    mysql = get_mysql(MYSQL)
    result = mysql.execute("INSERT INTO _object (`type`) VALUES (%s)", obj_type)
    #必须是自增列才能返回
    return result.lastrowid


def set_kvs(scope, kvs):
    if not hasattr(g, '_kvs_cache'):
        g._kvs_cache = {}

    if scope not in g._kvs_cache:
        g._kvs_cache[scope] = {}

    g._kvs_cache[scope].update(kvs)


def get_kv(scope, key):
    if hasattr(g, '_kvs_cache'):
        kvs = g._kvs_cache.get(scope)
        if kvs is not None:
            return kvs.get(key)


def _object_item_name(attr):
    return '_object_' + attr


def _collection_item_name(attr):
    return '_collection_' + attr


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if cls._name is not None:
            God._models[cls._name] = cls
            foreign_key = "{}_{}".format(cls._name, cls._pk)
            God._foreign_keys[foreign_key] = cls

        cls._fields = dict(zip(cls._fields, cls._fields))

        for field in cls._fields:
            if hasattr(field, 'object'):
                object_attr = field.object
                delattr(field, 'object')

                if cls._objects is None:
                    cls._objects = {}
                cls._objects[A(object_attr, **field.__dict__)] = field


class A(str):
    def __new__(cls, value, **kwargs):
        obj = str.__new__(cls, value)
        #该字段不返回给接口
        if kwargs.get('hidden') is not None:
            obj.hidden = kwargs.get('hidden')

        #该字段对应的对象名称，present的时候做展开并以该对象名替换该字段
        if kwargs.get('object') is not None:
            obj.object = kwargs.get('object')

        #foreign表示这个字段是外键否则就是扩展信息，伴随object出现
        if kwargs.get('foreign') is not None:
            obj.foreign = kwargs.get('foreign')

        #setter 编码存储 obj.attr = val => obj[attr] = setter(val)
        if kwargs.get('setter') is not None:
            obj.setter = partial(kwargs.get('setter'), value)

        #getter 解码显示 obj.attr => getter(obj[attr])
        if kwargs.get('getter') is not None:
            obj.getter = partial(kwargs.get('getter'), value)

        #表明是数据库字段
        if kwargs.get('column') is not None:
            obj.column = kwargs.get('column')

        return obj


class God(dict):
    """
    obj = Model(dict_data_from_db)

    #for inner usage
    obj[db_field]

    #for api presentation
    obj.field_attr : some value
    obj.object_attr : some model object
    obj.collection_attr(arg..)  : will call get_{collection_attr}(arg..) and cache in obj[collection_attr]
    obj.get_{collection_attr}(arg..) : same as above but no cache, must return a list

    #should be implemented method
    obj.get_id() : return object id
    obj.set_id(id) : set a object id and return self
    obj.find() : if obj.set_id(id) then get a only model object, else return collection of model object

    #setter
    obj.feed(attr=val,..)
    obj.object_attr = dict | model object
    obj.collection_attr = list|dict [,list|dict] : will call set_{collection_attr}(list) and cache in obj[collection_attr]
    set_{collection_attr}(list) : must return a list
    """
    __slots__ = ('mysql', '_fields_mod', '_add_delay')
    __metaclass__ = Meta
    #God 's properties
    #object_attr -> model class
    _models = {}
    #foreign_key -> model class
    _foreign_keys = {}

    #Model 's properties
    #object_attr -> field name of object id (dict)
    _objects = None

    #object_attr
    _name = None
    #object type id
    _type = None
    #db
    _db = MYSQL
    #table
    _table = None
    #primary key
    _pk = 'id'
    #field_attr -> field_attr
    _fields = ()
    #collection_attr (tuple)
    _collections = None

    def __init__(self, *args, **kwargs):
        super(God, self).__init__(*args, **kwargs)
        self.mysql = get_mysql(self._db)
        self._fields_mod = []
        self._add_delay = False

    def __getattr__(self, attr):
        #获取字段值
        if attr in self._fields:
            value = self.get(attr)
            if hasattr(self._fields[attr], 'getter'):
                return self._fields[attr].getter(self)
            return value

        #获取包含对象
        if self._objects is not None:
            field = self._objects.get(attr)
            #字段合法
            if field is not None:
                item_name = _object_item_name(attr)
                exist_data = self.get(item_name)
                #未获取数据
                if exist_data is None:
                    obj_id = self.get(field)
                    #含有外键
                    if obj_id:
                        model = God._models[attr]
                        exist_data = self[item_name] = model().set_id(obj_id).find()

                return exist_data

        if self._collections is not None \
                and attr in self._collections:
            return partial(self._collection, attr=attr)

        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

    def __setattr__(self, attr, value):
        if attr in self._fields:

            self._set_field_attr(attr, value)
        elif self._objects is not None \
                and attr in self._objects:

            self._set_object_attr(attr, value)
        elif self._collections is not None \
                and attr in self._collections:

            self._set_collection_attr(attr, value)

        elif attr in God.__slots__ or attr in self.__slots__:
            super(God, self).__setattr__(attr, value)

        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

    def _set_field_attr(self, attr, value):
        if hasattr(self._fields[attr], 'setter'):
            self._fields[attr].setter(self, value)
        else:
            self[attr] = value
        self._fields_mod.append(attr)

    def _set_object_attr(self, attr, value):
        field = self._objects.get(attr)

        if value is None:
            self._set_field_attr(field, None)
            self[_object_item_name(attr)] = None
            return

        model = God._models[attr]
        if isinstance(value, model):
            obj = value
        elif isinstance(value, dict):
            #外键不允许当成扩展
            if hasattr(field, 'foreign'):
                return
                #过滤
            if model._pk in value:
                value.pop(model._pk)
            if not value:
                return

            obj_id = getattr(self, field)
            if obj_id:
                #查找原来数据
                obj = model().set_id(obj_id).find()
                if not obj:
                    raise AttributeError("object with id {} is not exist".format(obj_id))
            else:
                #申请id
                obj = model().init()
                #执行存储
            obj.feed(**value)
            #只能设置有id的对象
        if obj.get_id():
            self._set_field_attr(field, obj.get_id())
            self[_object_item_name(attr)] = obj
        else:
            raise AttributeError("could not set object without id to attribute")

    def _set_collection_attr(self, attr, value):
        method = getattr(self.__class__, 'set_%s' % attr)
        if not isinstance(value, tuple):
            p = (value,)
        else:
            p = value
        self[_collection_item_name(attr)] = method(self, *p)

    def feed(self, **data):
        for attr, value in data.items():
            if value is not None and value != getattr(self, attr):
                setattr(self, attr, value)

        if self._add_delay:
            return self.add()
        else:
            return self.save()

    def _collection(self, attr, *args, **keywords):
        item_name = _collection_item_name(attr)
        exist_data = self.get(item_name)
        if exist_data is None:
            #数据未获取，重新获取
            method = getattr(self.__class__, 'get_%s' % attr)
            exist_data = self[item_name] = method(self, *args, **keywords)

        return exist_data

    def __len__(self):
        return bool(self.get_id())

    def get_id(self):
        return self.get(self._pk)

    def set_id(self, value):
        self[self._pk] = value

        return self

    def if_exists(self, where_fields):
        #条件字段
        if isinstance(where_fields, Where):
            where, values = where_fields.format(self)
            if not where:
                return False
        else:
            raise ValueError("param type must be 'Where'")

        result = self.mysql.execute("SELECT 0 FROM {} WHERE {} LIMIT 1".format(self._table, where), values)
        if result:
            return True
        else:
            return False

    def find(self, select_fields=None):
        """
        根据数据库字段，pager_ref 的引用，查询结束会更改其内容
        对主键进行的查询只返回对象本身
        """
        if self._table is not None:
            #根据主键获取记录
            if self.get_id():
                kvs = self.find_by_ids([self.get_id()])
                return kvs.get(self.get_id())
            else:
                return self.find_all(select_fields=select_fields, order_by='')
        else:
            raise NotImplementedError("method 'find()' was not implemented in '{}'".format(self.__class__.__name__))

    def _pk_statement(self, ids):
        if len(ids) == 1:
            return "{}.{} = {}".format(self._table, self._pk, ids[0])
        else:
            return "{}.{} IN ({})".format(self._table, self._pk, ','.join(ids))

    def _fetch_by_ids(self, non_cache_ids):
        """
        从数据库读取原始数据
        """

        fields = ','.join([self.escape_field(field) for field in self._fields])

        result = self.mysql.execute("SELECT {} FROM {} WHERE {}".format(fields,
                                                                        self._table,
                                                                        self._pk_statement(non_cache_ids)))

        return {row[self._pk]: self.__class__(row) for row in result.fetchall()}

    def find_by_ids_tuple(self, ids):
        """
        返回 缓存和未缓存数据分开
        """
        ids = [str(i) for i in set(ids) if i]
        if not ids:
            return {}, {}

        #缓存中直接获取
        cache_r = {}
        non_cache_ids = []
        for i in ids:
            obj = get_kv(self._table, int(i))
            if obj:
                cache_r[obj.get_id()] = obj
            else:
                non_cache_ids.append(i)

        if not non_cache_ids:
            return cache_r, {}

        kvs = self._fetch_by_ids(non_cache_ids)

        if kvs:
            set_kvs(self._table, kvs)

        return cache_r, kvs

    def find_by_ids(self, ids):
        """
        根据主键返回字典数据
        """
        cache_r, kvs = self.find_by_ids_tuple(ids)

        if kvs:
            cache_r.update(kvs)

        return cache_r

    def escape_field(self, field):
        if '.' not in field:
            return "{}.{}".format(self._table, field)
        else:
            return field

    def _fetch_all(self, calc, fields, where, order_by, limit, values):
        result = self.mysql.execute("SELECT {}{} FROM {} WHERE {} {} LIMIT {}".format(calc,
                                                                                      fields,
                                                                                      self._table,
                                                                                      where,
                                                                                      order_by,
                                                                                      limit),
                                    values)

        if calc:
            rows_found = self.mysql.rows_found()
        else:
            rows_found = None

        return [self.__class__(row) for row in result.fetchall()], rows_found

    def find_all(self, where_fields=None, select_fields=None, pager_ref=None, order_by=None):
        """
        根据给定的条件返回对象列表

        :type where_fields: And or Or or None
        :param where_fields: And('field1', Exp("`join_table.field`+`field2`<>%s", 'value1'))

        :type select_fields: list
        :param select_fields: ['field1','join_table.field']

        :type order_by: Exp or None or str
        :param order_by: Exp("`join_table.field` DESC")
        """
        #条件字段
        if not where_fields or isinstance(where_fields, Where):
            if not where_fields:
                self_fields = [field for field in self._fields if self.get(field) is not None]
                where_fields = And(*self_fields)

            where, values = where_fields.format(self)
            if not where:
                return []
        else:
            return []

        #选取字段
        if not select_fields:
            select_fields = self._fields

        fields = ','.join([self.escape_field(select_field) for select_field in select_fields])

        #默认主键排序
        if order_by is None:
            order_by = "ORDER BY {}.{} DESC".format(self._table, self._pk)
        elif isinstance(order_by, Exp):
            order_by, _ = order_by.format(self)
            order_by = "ORDER BY {}".format(order_by)

        #有分页要计算总记录数
        if pager_ref and pager_ref.offset is not None:
            calc = 'SQL_CALC_FOUND_ROWS '
            limit = '{},{}'.format(pager_ref.offset, pager_ref.limit)
        else:
            calc = ''
            limit = '{}'.format(Pager.MAX_LIMIT)

        r, rows_found = self._fetch_all(calc, fields, where, order_by, limit, values)

        #如果有分页
        if calc:
            pager_ref.rows_found = rows_found

        return r

    def _gen_id(self):
        if self._type is not None:
            return unique_id(self._type)
        else:
            return 0

    def init(self):
        self.set_id(self._gen_id())
        self._add_delay = True

        return self

    def validate(self):
        """
        字段校验，可在子类中实现
        """

    def add(self, fields_required=[]):
        """
        data can be obj or fields
        """
        self.validate()
        #非延迟添加且包含id，不允许调用
        if not self._add_delay and self.get_id():
            raise ValueError('could not add object with id')

        if 'ctime' in self._fields and self.get('ctime') is None:
            self['ctime'] = int(time.time())

        for field_required in fields_required:
            if self.get(field_required) is None:
                return False

        columns, params, values, _ = self._extract()

        #为全局对象申请自增id
        _id = None
        if not self.get_id() and self._type is not None:
            _id = self._gen_id()
            columns.append(self._pk)
            params.append('%s')
            values.append(_id)

        result = self.mysql.execute("INSERT INTO {} ({}) VALUES ({})".format(self._table,
                                                                             ','.join(columns),
                                                                             ','.join(params)), values)
        if result:
            self._add_delay = False
            #还未设置id
            if not self.get_id():
                if _id is not None:
                    self.set_id(_id)
                elif result.lastrowid:
                    self.set_id(result.lastrowid)
                else:
                    raise ValueError("table {} must have a auto increment column".format(self._table))

            return True

        return False

    def save(self, fields=None):
        """
        obj.field = new_value
        obj.save()
        """
        if fields is None:
            fields = self._fields_mod
            self.validate()

        _, _, values, pairs = self._extract(fields)

        if not values:
            return False

        values.append(self.get_id())
        return self.mysql.execute("UPDATE {} SET {} WHERE {}=%s".format(self._table,
                                                                        ','.join(pairs),
                                                                        self._pk), values)

    def delete(self):
        """
        根据主键删除对象
        """
        return self.delete_by_ids([self.get_id()])

    def delete_by_ids(self, ids):
        if len(ids) > 100:
            raise OverflowError('quantity exceeds limit')

        ids = [str(i) for i in set(ids) if int(i) > 0]
        if not ids:
            return True

        if len(ids) == 1:
            where = "{}={}"
        else:
            where = "{} IN ({})"
        self_where = where.format(self._pk, ','.join(ids))
        return self.mysql.execute("DELETE FROM {} WHERE {}".format(self._table, self_where))

    def _extract(self, fields=None):
        """
        格式化sql的格式
        """
        columns = []
        values = []

        if fields is None:
            fields = self.keys()

        for item_name in fields:
            if (item_name in self._fields or hasattr(item_name, 'column')) and self[item_name] is not None:
                columns.append('`' + item_name + '`')
                values.append(self[item_name])

        params = ['%s'] * len(columns)
        pairs = ['%s=%s' % (k, v) for k, v in zip(columns, params)]

        return columns, params, values, pairs

    def present(self):
        """
        输出成json格式

        God._objects 里面定义了 <object_name> : <foreign_key_name> 的映射;
        <object_name> 在 model 类里面 _name 定义;
        God._pk 获取对象的主键名称 <object_pk_name>;

        <foreign_key_name> : $id 将会按照 God._objects 里面的映射替换成 <object_name> : $object
        """
        data = {}
        fields = self._fields
        if self._objects is not None:
            fields = set(fields).difference(set(self._objects.values()))

        for field_attr in fields:
            if hasattr(field_attr, 'hidden'):
                continue

            val = getattr(self, field_attr)
            if val is not None:
                data[field_attr] = val

        if self._objects is not None:
            for object_attr in self._objects:
                if hasattr(object_attr, 'hidden'):
                    continue

                obj = getattr(self, object_attr) or self.get(object_attr)
                if obj:
                    if isinstance(obj, God):
                        data[object_attr] = obj.dump()
                    else:
                        data[object_attr] = obj

        #collections混合类型
        if self._collections is not None:
            for collection_attr in self._collections:
                if hasattr(collection_attr, 'hidden'):
                    continue

                method = getattr(self, collection_attr)
                col = method()
                if col is not None:
                    if isinstance(col, God):
                        col = col.dump()
                    elif isinstance(col, Array):
                        col = col.present()
                    elif isinstance(col, (types.TupleType, types.ListType, types.GeneratorType)):
                        ls = []
                        for obj in col:
                            if isinstance(col, God):
                                obj = obj.dump()
                            ls.append(obj)
                        col = ls

                    data[collection_attr] = col

        return self.dump(data)

    def dump(self, object_dict=None):
        """
        God._foreign_keys 里面定义了 <foreign_key_name> : model

        打印 <(dict) self> 或者 object_dict 的值，并把
        <foreign_key_name> : $id 按照 God._foreign_keys 里的映射替换为 <object_name> : {<object_pk_name> : $id}
        """
        if object_dict is None:
            object_dict = self

        data = {}
        for k, v in object_dict.items():
            if v is None:
                continue

            if k in self._fields:
                if hasattr(self._fields[k], 'hidden'):
                    continue

            model = God._foreign_keys.get(k)
            if model is not None:
                object_attr, pk_name = model._name, model._pk
                if data.get(object_attr) is None and v:
                    data[object_attr] = {pk_name: v}

                continue

            if k.startswith('_collection_'):
                k = k[12:]
                if k in self._collections:
                    k_idx = self._collections.index(k)
                    if hasattr(self._collections[k_idx], 'hidden'):
                        continue

                if isinstance(v, God):
                    v = v.dump()

            if k.startswith('_object_'):
                k = k[8:]
                if k in self._objects:
                    if hasattr(self._objects[k], 'hidden'):
                        continue

                if isinstance(v, God):
                    v = v.dump()

            data[k] = v

        return data

    @contextmanager
    def transaction(self):
        self.mysql.begin()
        try:
            yield
            self.mysql.commit()
        finally:
            self.mysql.rollback()


class Array(tuple):
    """
    将Array里面的对象的外键收集起来，一次性查询出来，获取每个的dump结果，组装在一起
    """

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls)

    def __init__(self, model, iterable=None):
        if not issubclass(model, God):
            raise ValueError('Array is only for subclass of God')
        self.model = model

        self.data = []
        if iterable is not None:
            if isinstance(iterable, (types.TupleType, types.ListType, types.GeneratorType)):
                for obj in iterable:
                    self.append(obj)
            else:
                raise ValueError('arg is not iterable')

    def append(self, obj):
        if not isinstance(obj, self.model):
            obj = self.model(obj)
        self.data.append(obj)

    def __len__(self):
        return len(self.data)

    def present(self):
        if self.model._objects:
            for object_attr, foreign_key in self.model._objects.items():
                ids = [getattr(obj, foreign_key) for obj in self.data]
                foreign_model = God._models[object_attr]

                foreign_model().find_by_ids(ids)

        return [obj.present() for obj in self.data]

