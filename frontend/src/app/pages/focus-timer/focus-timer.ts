import { Component, signal, computed } from '@angular/core';

@Component({
  selector: 'app-focus-timer',
  imports: [],
  templateUrl: './focus-timer.html',
  styleUrl: './focus-timer.css'
})
export class FocusTimer {
  hours = signal(0);
  minutes = signal(25);
  seconds = signal(0);
  holdInterval: any;

  remainingSeconds = signal(25 * 60);
  initialTotalSeconds = signal(25 * 60);

  isRunning = signal(false);
  timerInterval: any;

  totalInputSeconds = computed(() =>
    this.hours() * 3600 + this.minutes() * 60 + this.seconds()
  );

  progressPercent = computed(() => {
    if (this.initialTotalSeconds() === 0) {
      return 0;
    }

    return (this.remainingSeconds() / this.initialTotalSeconds()) * 100;
  });

  formattedTime = computed(() => {
    const hrs = Math.floor(this.remainingSeconds() / 3600);
    const mins = Math.floor((this.remainingSeconds() % 3600) / 60);
    const secs = this.remainingSeconds() % 60;

    return `${hrs.toString().padStart(2, '0')}:${mins
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  });

  increaseHours(): void {
    this.hours.update(value => value + 1);
    this.syncInputToTimer();
  }

  decreaseHours(): void {
    this.hours.update(value => Math.max(0, value - 1));
    this.syncInputToTimer();
  }

  increaseMinutes(): void {
    this.minutes.update(value => Math.min(59, value + 1));
    this.syncInputToTimer();
  }

  decreaseMinutes(): void {
    this.minutes.update(value => Math.max(0, value - 1));
    this.syncInputToTimer();
  }

  increaseSeconds(): void {
    this.seconds.update(value => Math.min(59, value + 1));
    this.syncInputToTimer();
  }

  decreaseSeconds(): void {
    this.seconds.update(value => Math.max(0, value - 1));
    this.syncInputToTimer();
  }

  syncInputToTimer(): void {
    if (this.isRunning()) {
      return;
    }

    const total = this.totalInputSeconds();

    this.remainingSeconds.set(total);
    this.initialTotalSeconds.set(total);
  }

  startTimer(): void {
    if (this.isRunning() || this.remainingSeconds() <= 0) {
      return;
    }

    this.isRunning.set(true);

    this.timerInterval = setInterval(() => {
      if (this.remainingSeconds() > 0) {
        this.remainingSeconds.update(value => value - 1);
      } else {
        this.pauseTimer();
      }
    }, 1000);
  }

  pauseTimer(): void {
    clearInterval(this.timerInterval);
    this.isRunning.set(false);
  }

  resetTimer(): void {
    this.pauseTimer();
    this.syncInputToTimer();
  }

  startHold(action: () => void): void {
    action();

    this.holdInterval = setInterval(() => {
      action();
    }, 150);
  }

  stopHold(): void {
    clearInterval(this.holdInterval);
  }

  holdIncreaseHours(): void {
    this.startHold(() => this.increaseHours());
  }

  holdDecreaseHours(): void {
    this.startHold(() => this.decreaseHours());
  }

  holdIncreaseMinutes(): void {
    this.startHold(() => this.increaseMinutes());
  }

  holdDecreaseMinutes(): void {
    this.startHold(() => this.decreaseMinutes());
  }

  holdIncreaseSeconds(): void {
    this.startHold(() => this.increaseSeconds());
  }

  holdDecreaseSeconds(): void {
    this.startHold(() => this.decreaseSeconds());
  }

  timerColor = computed(() => {
    const progress = this.progressPercent();

    if (progress <= 10) {
      return 'red';
    }

    if (progress <= 30) {
      return 'orange';
    }

    if (progress <= 60) {
      return 'gold';
    }

    return 'blue';
  });
}