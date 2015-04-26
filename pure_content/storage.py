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
        return os.path.join(self._storage_directory, *keys)

    @classmethod
    def _get_default_storage_directory(cls):
        return os.path.join(os.getcwd(), 'data')

    def load_resource(self, path, resource):
        with open(path, 'r') as resource_file:
            resource.content = resource_file.read()

    def save_resource(self, path, resource):
        resource_directory = os.path.dirname(path)
        if not os.path.exists(resource_directory):
            os.makedirs(resource_directory)
        if resource.is_text:
            mode = 'w+'
            content = resource.content.encode('utf-8')
        else:
            mode = 'wb+'
            content = resource.content
        with open(path, mode=mode) as resource_file:
            resource_file.write(content)


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
    def __init__(self, container, content=None, text_content=True):
        ResourceBase.__init__(self, container, content)
        self._is_text = text_content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def is_item(self):
        return True

    @property
    def is_text(self):
        return self._is_text


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


class Images(CollectionResource):
    def __init__(self, container, images):
        content = {}
        urls = []
        for image_name, image_item in images.items():
            content[image_name] = ItemResource(
                container=self,
                content=image_item['content'],
                text_content=False,
            )
            url = image_item['url']
            urls.append((url, image_name))
        urls_content = u'\n'.join(
            u'{file_name} <- {url}'.format(
                url=url,
                file_name=file_name
            ) for url, file_name in urls
        )
        content['urls.log'] = ItemResource(self, urls_content)
        CollectionResource.__init__(self, container, content)


class Container(CollectionResource):
    def __init__(self, url, title, text, images=None):
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
        if images:
            content['images'] = Images(self, images)
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
