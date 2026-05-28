import { Component, signal, OnInit, computed, NgZone } from '@angular/core';
import { TaskService, Task } from '../../services/task';

@Component({
  selector: 'app-tasks',
  imports: [],
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.css'
})
export class Tasks implements OnInit {
  tasks = signal<Task[]>([]);
  brainDump = signal('');
  selectedActiveTaskIds = signal<string[]>([]);
  selectedCompletedTaskIds = signal<string[]>([]);
  recognition: any;
  editingTaskId = signal<string | null>(null);
  editTitle = signal(``);
  editDueDate = signal(``);
  editUrgency = signal(`normal`);

  constructor(
    private taskService: TaskService,
    private ngZone: NgZone
  ) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  activeTasks = computed(() =>
    this.tasks().filter(task => !task.completed)
  );

  completedTasks = computed(() =>
    this.tasks().filter(task => task.completed)
  );

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
      alert('Speech recognition is not supported in this browser.');
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

  toggleActiveTaskSelection(taskId: string): void {
    this.selectedActiveTaskIds.update(ids =>
      ids.includes(taskId)
        ? ids.filter(id => id !== taskId)
        : [...ids, taskId]
    );
  }

  toggleCompletedTaskSelection(taskId: string): void {
    this.selectedCompletedTaskIds.update(ids =>
      ids.includes(taskId)
        ? ids.filter(id => id !== taskId)
        : [...ids, taskId]
    );
  }

  completeSelectedTasks(): void {
    const taskIds = this.selectedActiveTaskIds();

    if (!taskIds.length) {
      return;
    }

    this.taskService.completeTasks(taskIds).subscribe({
      next: () => {
        this.selectedActiveTaskIds.set([]);
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error completing tasks:', error);
      }
    });
  }

  restoreSelectedTasks(): void {
    const taskIds = this.selectedCompletedTaskIds();

    if (!taskIds.length) {
      return;
    }

    this.taskService.restoreTasks(taskIds).subscribe({
      next: () => {
        this.selectedCompletedTaskIds.set([]);
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error restoring tasks:', error);
      }
    });
  }

  deleteSelectedActiveTasks(): void {
    const taskIds = this.selectedActiveTaskIds();

    if (!taskIds.length) {
      return;
    }

    if (!confirm(`Delete ${taskIds.length} selected active taskIds(s)?`)) {
        return;
      }

    this.taskService.deleteTasks(taskIds).subscribe({
      next: () => {
        this.selectedActiveTaskIds.set([]);
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error deleting active tasks:', error);
      }
    });
  }

  deleteSelectedCompletedTasks(): void {
    const taskIds = this.selectedCompletedTaskIds();

    if (!taskIds.length) {
      return;
    }

    if (!confirm(`Delete ${taskIds.length} selected history task(s)?`)) {
      return;
    }

    this.taskService.deleteTasks(taskIds).subscribe({
      next: () => {
        this.selectedCompletedTaskIds.set([]);
        this.loadTasks();
      },
      error: (error) => {
        console.error('Error deleting completed tasks:', error);
      }
    });
  }

  startEditingTask(task: Task): void {
    this.editingTaskId.set(task.id);
    this.editTitle.set(task.title);
    this.editDueDate.set(task.due_date || ``);
    this.editUrgency.set(task.urgency || `normal`);
  }

  cancelEditingTask(): void {
    this.editingTaskId.set(null);
    this.editTitle.set(``);
    this.editDueDate.set(``);
    this.editUrgency.set(`normal`);
  }

  saveEditedTask(): void {
    const taskId = this.editingTaskId();

    if (!taskId) {
      return;
    }

    this.taskService.updateTask(taskId, {
      title: this.editTitle().trim(),
      due_date: this.editDueDate().trim() || null,
      urgency: this.editUrgency()
    }).subscribe({
      next: () => {
        this.cancelEditingTask();
        this.loadTasks();
      },
      error: (error) => {
        console.error(`Error updating task:`, error);
      }
    });
  }

  canEditSelectedActiveTask = computed(() =>
    this.selectedActiveTaskIds().length === 1
  );

  startEditingSelectedTask(): void {
    const selectedId = this.selectedActiveTaskIds()[0];

    if (!selectedId) {
      return;
    }

    const task = this.tasks().find(task => task.id === selectedId);

    if (!task) {
      return;
    }

    this.startEditingTask(task);
  }
}