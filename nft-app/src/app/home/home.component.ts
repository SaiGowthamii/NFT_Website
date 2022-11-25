import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import {NftserService} from '../nftser.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  menuopt: any[] ;
  ethadd:any;
  token_id:any;
  selectedCity:any;
  sales: any=[];
  result:any[]=[];
  userDetails:any=[];
  display:boolean=false;
  showData:boolean=false;
  showLoader:boolean=false;
  selected:any;
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  
  constructor(private router:Router,private nftService:NftserService) {
    this.homepage();
    this.menuopt = [
      {name: 'Home', code: 'HM',},
      {name: 'Own NFT', code: 'OT'},
      {name: 'Transaction History', code: 'TRH'},
      {name: 'Wallet (Add/Withdraw)', code:'WA'}
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
  homepage(){
   this.userDetails=localStorage.getItem('t_id');
   console.log(this.userDetails);
   this.showLoader=true;
    this.nftService.homeApi(this.userDetails).subscribe(data=>{
      this.showLoader=false;
         for(let i in data){
          let temp={
                'nft_name':data[i].nft_name,
                'contract_addr':data[i].contract_addr,
                'token_id' :data[i].token_id,
                'current_price':data[i].current_price
              }
              this.sales.push(temp);
         }
      console.log(this.sales)
      
       });

  }

  search(){
    this.showLoader=true;
    if(this.token_id!='' || this.ethadd!=''){
      for(let i=0;i<this.sales.length;i++){
        if(this.sales[i].contract_addr==this.ethadd && this.sales[i].token_id==this.token_id){
          let temp={
            'nft_name':this.sales[i].nft_name,
            'contract_addr':this.sales[i].contract_addr,
            'token_id' :this.sales[i].token_id,
            'current_price':this.sales[i].current_price
          }
          this.result.push(temp);
        }
        else if(this.result.length <0) {
          this.result=[];
        }
      }
      this.showLoader=false;
      this.sales=this.result;
    }

  }
  reset(){
   this.ethadd=null;
   this.token_id=null;
   this.homepage();
  }
  onChange(e:any){
    console.log("Event",e);
    if(e.value.code=='OT') {
      this.selected=e.value.name;
      this.router.navigate(['/own']);
    }
    else if(e.value.code=='WA') {
      this.router.navigate(['/addTowallet']);
    }
    else if(e.value.code=='TRH') {
      this.router.navigate(['/history']);
    }
  }

  

}
