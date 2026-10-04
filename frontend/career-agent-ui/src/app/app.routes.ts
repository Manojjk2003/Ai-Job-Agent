import { Routes } from '@angular/router';
import { ProfileComponent } from './features/profile/profile.component';

export const routes: Routes = [{path:'profile',component:ProfileComponent},{path:'',pathMatch:'full',redirectTo:'profile'}];
