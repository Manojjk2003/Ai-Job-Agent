from abc import ABC,abstractmethod
class OutreachProvider(ABC):
 name:str
 @abstractmethod
 def prepare(self,context:dict)->dict:...
class ManualOutreachProvider(OutreachProvider):
 name='manual_template'
 def prepare(self,context):return {'subject':f"Interest in {context['job_title']}",'body':f"Hello,\n\nI am reaching out regarding the {context['job_title']} role at {context['company_name']}.\n\nThank you."}
