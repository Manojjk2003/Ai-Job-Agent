import { Routes } from '@angular/router';
import { ProfileComponent } from './features/profile/profile.component';
import { SkillsComponent } from './features/profile/skills.component';
import { ResumesComponent } from './features/profile/resumes.component';

export const routes: Routes = [{path:'profile',component:ProfileComponent},{path:'skills',component:SkillsComponent},{path:'resumes',component:ResumesComponent},{path:'',pathMatch:'full',redirectTo:'profile'}];
