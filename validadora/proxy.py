class MetaProxy(type):
  _members = {}

  def _get_members_func(cls):
      return cls._members

  def __getattr__(cls, item):
      print(item)
      if 'members' == item:
          return cls._get_members_func()

      if item in cls._members.keys():
          return cls._members.get(item)


  def __setattr__(cls, key, value):
      print(key)
      if not cls._members.get(key, False):
          cls._members[key] = value


class Proxy(metaclass=MetaProxy):
  pass
