import { Component, signal, OnInit, computed, NgZone } from '@angular/core';
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
  selectedTaskId = signal('');
  recognition: any;

  constructor(
    private taskService: TaskService,
    private ngZone: NgZone
  ) {}

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

  startVoiceRecognition(): void {
    const SpeechRecognition = 
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in this browser.')
      return;
    }

    this.recognition = new SpeechRecognition();

    this.recognition.lang = 'en-US';
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;

    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      
      console.log('Transcript:', transcript);

      this.ngZone.run(() => {
        this.brainDump.set(transcript);
      });
    };

    this.recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
    };

    this.recognition.start();
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
