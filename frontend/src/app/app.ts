import { Component, signal, OnInit } from '@angular/core';
import { TaskService, Task } from './services/task';


@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App implements OnInit {
  tasks = signal<Task[]>([]);

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
      this.taskService.getTasks().subscribe({
        next: (response) => {
          console.log('Tasks response:', response);
          this.tasks.set(response.tasks);
        },
        error: (error) => {
          console.error('Error loading tasks:', error);
        }
      });
  }
}
