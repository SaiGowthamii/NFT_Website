import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddTowalletComponent } from './add-towallet.component';

describe('AddTowalletComponent', () => {
  let component: AddTowalletComponent;
  let fixture: ComponentFixture<AddTowalletComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddTowalletComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddTowalletComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
