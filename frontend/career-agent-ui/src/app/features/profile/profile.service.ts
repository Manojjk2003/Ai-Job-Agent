import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
export interface Profile { phone?: string; location?: string; headline?: string; summary?: string; years_experience?: number; current_designation?: string; linkedin_url?: string; github_url?: string; }
export interface Experience { id: string; company_name: string; job_title: string; start_date: string; end_date?: string; is_current: boolean; description?: string; display_order: number; }
export interface Education { id: string; institution: string; degree?: string; field_of_study?: string; display_order: number; }
export interface Project { id: string; name: string; role?: string; project_type?: string; display_order: number; }
@Injectable({providedIn:'root'}) export class ProfileService {
  private readonly base='/api/v1/profile'; constructor(private http:HttpClient) {}
  get():Observable<Profile|null>{return this.http.get<Profile|null>(this.base)} update(value:Profile){return this.http.put<Profile>(this.base,value)}
  experiences(){return this.http.get<Experience[]>(`${this.base}/experiences`)} createExperience(value:Omit<Experience,'id'>){return this.http.post<Experience>(`${this.base}/experiences`,value)} deleteExperience(id:string){return this.http.delete(`${this.base}/experiences/${id}`)}
  education(){return this.http.get<Education[]>(`${this.base}/education`)} projects(){return this.http.get<Project[]>(`${this.base}/projects`)}
}
