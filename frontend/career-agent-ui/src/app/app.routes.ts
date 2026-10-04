import { Routes } from '@angular/router';
import { ProfileComponent } from './features/profile/profile.component';
import { SkillsComponent } from './features/profile/skills.component';

export const routes: Routes = [{path:'profile',component:ProfileComponent},{path:'skills',component:SkillsComponent},{path:'',pathMatch:'full',redirectTo:'profile'}];
