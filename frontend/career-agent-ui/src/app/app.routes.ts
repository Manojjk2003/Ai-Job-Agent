import { Routes } from '@angular/router';
import { ProfileComponent } from './features/profile/profile.component';
import { SkillsComponent } from './features/profile/skills.component';
import { ResumesComponent } from './features/profile/resumes.component';
import { RoleProfilesComponent } from './features/profile/role-profiles.component';
import { PreferencesComponent } from './features/profile/preferences.component';
import { CompaniesComponent } from './features/profile/companies.component';
import { JobsComponent } from './features/profile/jobs.component';
import { ApplicationsComponent } from './features/profile/applications.component';
import { OutreachComponent } from './features/profile/outreach.component';
import { CommunicationsComponent } from './features/profile/communications.component';
import { AnalyticsComponent } from './features/profile/analytics.component';

export const routes: Routes = [{path:'profile',component:ProfileComponent},{path:'skills',component:SkillsComponent},{path:'resumes',component:ResumesComponent},{path:'role-profiles',component:RoleProfilesComponent},{path:'preferences',component:PreferencesComponent},{path:'companies',component:CompaniesComponent},{path:'jobs',component:JobsComponent},{path:'applications',component:ApplicationsComponent},{path:'outreach',component:OutreachComponent},{path:'communications',component:CommunicationsComponent},{path:'analytics',component:AnalyticsComponent},{path:'',pathMatch:'full',redirectTo:'profile'}];
