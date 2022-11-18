import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  menuopt: any[] ;
  selectedCity:any;
  sales: any[];
  display:boolean=false;
  constructor(private router:Router) {
    this.menuopt = [
      {name: 'Home', code: 'HM'},
      {name: 'Own NFT', code: 'OT'},
      {name: 'Transaction History', code: 'TRH'},
  ];
  this.sales = [
    { code: 'Apple', name: '51%', category: '40%', quantity: '$54,406.00' },
    { code: 'Samsung', name: '83%', category: '96%', quantity: '$423,132' },
    { code: 'Microsoft', name: '38%', category: '5%', quantity: '$12,321' },
    { code: 'Philips', name: '49%', category: '22%', quantity: '$745,232' },
    { code: 'Song', name: '17%', category: '79%', quantity: '$643,242' },
    { code: 'LG', name: '52%', category: ' 65%', quantity: '$421,132' },
    { code: 'Sharp', name: '82%', category: '12%', quantity: '$131,211' },
    { code: 'Panasonic', name: '44%', category: '45%', quantity: '$66,442' },
    { code: 'HTC', name: '90%', category: '56%', quantity: '$765,442'},
    { code: 'Toshiba', name: '75%', category: '54%', quantity: '$21,212' }
];
   }

  ngOnInit(): void {
    
  }
  login(){
    this.router.navigate(['/login']);
  }
  buy(event:any){
    console.log("event",event);
    this.display=true
  }
  

}
