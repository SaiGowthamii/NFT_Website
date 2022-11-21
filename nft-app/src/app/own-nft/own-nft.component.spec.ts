import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnNftComponent } from './own-nft.component';

describe('OwnNftComponent', () => {
  let component: OwnNftComponent;
  let fixture: ComponentFixture<OwnNftComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OwnNftComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OwnNftComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
