import { TestBed } from '@angular/core/testing';

import { NftserService } from './nftser.service';

describe('NftserService', () => {
  let service: NftserService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NftserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
