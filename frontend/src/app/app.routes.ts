import { Routes } from '@angular/router';
import { Tasks } from './pages/tasks/tasks';
import { FocusTimer } from './pages/focus-timer/focus-timer';

export const routes: Routes = [
  {
    path: 'tasks',
    component: Tasks
  },
  {
    path: '',
    redirectTo: 'tasks',
    pathMatch: 'full'
  }
];
