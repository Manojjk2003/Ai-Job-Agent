from abc import ABC,abstractmethod
from dataclasses import dataclass
@dataclass(frozen=True)
class ProviderHiringSource: name:str;source_type:str;source_url:str;external_reference:str|None=None;notes:str|None=None
class HiringSourceProvider(ABC):
 name:str
 @abstractmethod
 def discover_sources(self,sources:list[ProviderHiringSource])->list[ProviderHiringSource]:pass
 def health_check(self)->bool:return True
class UserProvidedHiringSourceProvider(HiringSourceProvider):
 name='user_provided'
 def discover_sources(self,sources):return sources
