import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
export type Proficiency='beginner'|'intermediate'|'advanced'|'expert';
export interface Skill {id:string;name:string;category:string}
export interface CandidateSkill {id:string;skill_id:string;proficiency?:Proficiency;years_experience?:number;is_primary:boolean}
export interface Evidence {id:string;evidence_type:'experience'|'project'|'education'|'certification'|'candidate_claim';reference_id?:string;description?:string}
@Injectable({providedIn:'root'}) export class SkillsService {constructor(private http:HttpClient){}
 search(q=''){return this.http.get<Skill[]>(`/api/v1/skills?search=${encodeURIComponent(q)}`)} list(){return this.http.get<CandidateSkill[]>('/api/v1/profile/skills')}
 add(v:Omit<CandidateSkill,'id'>){return this.http.post<CandidateSkill>('/api/v1/profile/skills',v)} update(id:string,v:Omit<CandidateSkill,'id'>){return this.http.put<CandidateSkill>(`/api/v1/profile/skills/${id}`,v)} delete(id:string){return this.http.delete(`/api/v1/profile/skills/${id}`)}
 evidence(id:string){return this.http.get<Evidence[]>(`/api/v1/profile/skills/${id}/evidence`)} addEvidence(id:string,v:Omit<Evidence,'id'>){return this.http.post<Evidence>(`/api/v1/profile/skills/${id}/evidence`,v)} deleteEvidence(id:string,evidenceId:string){return this.http.delete(`/api/v1/profile/skills/${id}/evidence/${evidenceId}`)} }
