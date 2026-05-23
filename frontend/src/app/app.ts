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
  brainDump = signal('');

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
      this.loadTasks();
  }

  loadTasks(): void {
    this.taskService.getTasks().subscribe({
      next: (response) => {
        this.tasks.set(response.tasks);
      },
      error: (error) => {
        console.error('Error loading tasks:', error);
      }
    });
  }

  submitBrainDump(): void {
    const text = this.brainDump().trim();

    if (!text) {
      return;
    }

    this.taskService.parseTasks(text).subscribe({
      next: () => {
        this.brainDump.set('');
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error parsing tasks:', error);
      }
    });
  }
}
