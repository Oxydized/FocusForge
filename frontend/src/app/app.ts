import { Component, signal, OnInit, computed } from '@angular/core';
import { TaskService, Task } from './services/task';
import { Observable } from 'rxjs';



@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App implements OnInit {
  tasks = signal<Task[]>([]);
  brainDump = signal('');
  selectedTaskId = signal('');

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

  completeSelectedTask(): void {
    const taskId = this.selectedTaskId();

    if (!taskId) {
      return;
    }

    this.taskService.completeTask(taskId).subscribe({
      next: () =>  {
        this.selectedTaskId.set('');
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error completing task:', error); 
      }
    });
  }

  activeTasks = computed(() => 
    this.tasks().filter(task => !task.completed)
  );

  completedTasks = computed(() => 
    this.tasks().filter(task => task.completed)
  );

  restoreTask(taskId: string): void {
    this.taskService.restoreTask(taskId).subscribe({
      next: () => {
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error restoring task:', error);
      }
    });
  }
}
