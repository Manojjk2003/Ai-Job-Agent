import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

export interface CompanyLocation {id?:string; location_name:string; area?:string; city?:string; state?:string; country?:string; location_type?:'headquarters'|'office'|'branch'|'remote'|'unknown'; is_headquarters?:boolean;}
export interface Company {id:string; canonical_name:string; website_url?:string; website_domain?:string; description?:string; industry?:string; company_size?:string; company_stage?:string; status:'active'|'inactive'|'unknown'; confidence:'low'|'medium'|'high'; locations:CompanyLocation[]; updated_at:string;}
export interface CompanyDraft {name:string; website_url?:string; description?:string; industry?:string; locations:CompanyLocation[]; status?:'active'|'inactive'|'unknown';}
export interface DiscoveryRun {id:string; location_name:string; provider_name:string; status:string; result_count:number; error_message?:string;}
export interface DiscoveryResponse {run:DiscoveryRun; companies:Company[];}

@Injectable({providedIn:'root'})
export class CompaniesService {
  constructor(private http:HttpClient) {}
  list(search?:string, city?:string){return this.http.get<Company[]>('/api/v1/companies',{params:{...(search?{search}:{}),...(city?{city}:{})}})}
  get(id:string){return this.http.get<Company>(`/api/v1/companies/${id}`)}
  create(value:CompanyDraft){return this.http.post<Company>('/api/v1/companies',value)}
  discover(location:CompanyLocation, companies:CompanyDraft[]){return this.http.post<DiscoveryResponse>('/api/v1/companies/discover',{location,companies})}
  runs(){return this.http.get<DiscoveryRun[]>('/api/v1/companies/discovery-runs')}
}
