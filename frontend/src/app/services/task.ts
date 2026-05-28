import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Task {
  id: string;
  title: string;
  due_date: string | null;
  urgency: string;
  completed: boolean;
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

  parseTasks(text: string): Observable<{ message: string; tasks: Task[]; total_tasks: number }> {
    return this.http.post<{ message: string; tasks: Task[]; total_tasks: number }>(
      `${this.apiURL}/tasks/parse`,
      { text }
    );
  }
  
  completeTasks(taskIds: string[]): Observable<{ message: string }> {
    return this.http.patch<{ message: string}>(
      `${this.apiURL}/tasks/complete`,
      { task_ids: taskIds }
    );
  }

  restoreTasks(taskIds: string[]): Observable<{ message: string }> {
    return this.http.patch<{ message: string }>(
      `${this.apiURL}/tasks/restore`,
      { task_ids: taskIds}
    );
  }
  
  deleteTasks(taskIds: string[]): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(
      `${this.apiURL}/tasks`,
      {
        body: { task_ids: taskIds}
      }
    );
  }

  updateTask(taskId: string, updates: Partial<Pick<Task, `title` | `due_date` | `urgency`>>
  ): Observable<{ message: string; task: Task }> {
    return this.http.patch<{ message: string; task: Task }>(
      `${this.apiURL}/tasks/${taskId}`,
      updates
    );
  }
}
