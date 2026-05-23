import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FocusTimer } from './focus-timer';

describe('FocusTimer', () => {
  let component: FocusTimer;
  let fixture: ComponentFixture<FocusTimer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FocusTimer],
    }).compileComponents();

    fixture = TestBed.createComponent(FocusTimer);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
