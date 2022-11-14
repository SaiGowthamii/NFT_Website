import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  menuopt: any[] ;
  selectedCity:any;

  constructor() {
    this.menuopt = [
      {name: 'Home', code: 'HM'},
      {name: 'Own NFT', code: 'OT'},
      {name: 'Transaction History', code: 'TRH'},
  ];
   }

  ngOnInit(): void {
    
  }
  

}
