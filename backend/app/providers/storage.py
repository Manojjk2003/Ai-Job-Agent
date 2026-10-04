from abc import ABC,abstractmethod
from pathlib import Path
class StorageProvider(ABC):
 @abstractmethod
 def save(self,key:str,data:bytes)->None:...
 @abstractmethod
 def read(self,key:str)->Path:...
 @abstractmethod
 def delete(self,key:str)->None:...
class LocalStorageProvider(StorageProvider):
 def __init__(self,root:str):self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
 def _path(self,key):
  path=(self.root/key).resolve()
  if self.root not in path.parents:return None
  return path
 def save(self,key,data):
  path=self._path(key)
  if path is None:raise ValueError('Unsafe storage key')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 def read(self,key):
  path=self._path(key)
  if path is None or not path.is_file():raise FileNotFoundError(key)
  return path
 def delete(self,key):
  path=self._path(key)
  if path is None:raise ValueError('Unsafe storage key')
  if path.exists():path.unlink()
