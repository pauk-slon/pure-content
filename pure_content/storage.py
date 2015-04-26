# -*- coding: utf-8 -*-
import os
from hashlib import md5


class StorageManager(object):
    def __init__(self, storage_directory=None):
        if storage_directory is None:
            self._storage_directory = self._get_default_storage_directory()
        else:
            self._storage_directory = storage_directory

    @classmethod
    def _get_default_storage_directory(cls):
        raise NotImplementedError()

    def load_resource(self, path, resource):
        raise NotImplementedError()

    def save_resource(self, path, resource):
        raise NotImplementedError()

    def get_path(self, keys):
        raise NotImplementedError()


class FileStorageManager(StorageManager):
    def get_path(self, keys):
        return u'{storage_directory}{sep}{resource_rel_path}'.format(
            storage_directory=self._storage_directory,
            sep=os.path.sep,
            resource_rel_path=os.path.sep.join(keys),
        )

    @classmethod
    def _get_default_storage_directory(cls):
        return u'{working_directory}{sep}data'.format(
            working_directory=os.getcwd(),
            sep=os.path.sep,
        )

    def load_resource(self, path, resource):
        with open(path, 'r') as resource_file:
            resource.content = resource_file.read()

    def save_resource(self, path, resource):
        resource_directory = os.path.dirname(path)
        if not os.path.exists(resource_directory):
            os.makedirs(resource_directory)
        with open(path, 'w+') as resource_file:
            resource_file.write(resource.content.encode('utf-8'))


class ResourceBase(object):
    def __init__(self, container, content=None):
        self._container = container
        self._content = content

    @property
    def container(self):
        return self._container

    @property
    def is_item(self):
        raise NotImplementedError()


class ItemResource(ResourceBase):
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def is_item(self):
        return True


class CollectionResource(ResourceBase):
    def __init__(self, container, content={}):
        ResourceBase.__init__(self, container, content)

    def __getitem__(self, key):
        return self._content[key]

    def items(self):
        return self._content.items()

    @property
    def is_item(self):
        return False


class Container(CollectionResource):
    def __init__(self, url, title, text):
        self.storage_manager = FileStorageManager()
        text_md5 = md5(text.encode('utf-8'))
        self._name = text_md5.hexdigest()
        url_content = u'[InternetShortcut]\nURL={url}\n'.format(
            url=url
        )
        content = {
            'article.url': ItemResource(self, url_content),
            'article.title': ItemResource(self, title),
            'article.txt': ItemResource(self, text),
        }
        CollectionResource.__init__(self, None, content)

    @property
    def name(self):
        return self._name

    def _fill_child_list(self, children, keys, resource):
        if resource.is_item:
            children.append((keys, resource))
        else:
            for key, value in resource.items():
                self._fill_child_list(children, keys + [key], value)

    def save(self):
        child_list = []
        self._fill_child_list(child_list, [self.name], self)
        for keys, resource in child_list:
            path = self.storage_manager.get_path(keys)
            self.storage_manager.save_resource(path, resource)

    def get_path(self):
        return self.storage_manager.get_path([self.name])
