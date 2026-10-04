import { Routes } from '@angular/router';
import { ProfileComponent } from './features/profile/profile.component';
import { SkillsComponent } from './features/profile/skills.component';
import { ResumesComponent } from './features/profile/resumes.component';
import { RoleProfilesComponent } from './features/profile/role-profiles.component';
import { PreferencesComponent } from './features/profile/preferences.component';

export const routes: Routes = [{path:'profile',component:ProfileComponent},{path:'skills',component:SkillsComponent},{path:'resumes',component:ResumesComponent},{path:'role-profiles',component:RoleProfilesComponent},{path:'preferences',component:PreferencesComponent},{path:'',pathMatch:'full',redirectTo:'profile'}];
