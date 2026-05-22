import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Task {
  id: string;
  title: string;
  due_date: string | null;
  urgency: string;
  completed: boolean
}

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private apiURL = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getTasks(): Observable<{ tasks: Task[] }> {
    return this.http.get<{ tasks: Task[] }>(`${this.apiURL}/tasks`);
  }
}
