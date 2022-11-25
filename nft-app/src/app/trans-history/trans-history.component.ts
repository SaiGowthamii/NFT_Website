import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NftserService } from '../nftser.service';

@Component({
  selector: 'app-trans-history',
  templateUrl: './trans-history.component.html',
  styleUrls: ['./trans-history.component.scss']
})
export class TransHistoryComponent implements OnInit {
  menuopt: any[] ;
  ethadd:any;
  token_id:any;
  selectedCity:any;
  sales: any=[];
  result:any[]=[];
  userDetails:any=[];
  display:boolean=false;
  selectedwBtn:boolean=true;
  selectedNBtn:boolean=false;
  side_bar:boolean=true;
  showData:boolean=false;
  showLoader:boolean=false;
  selected:any;
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  constructor(private router:Router,private nftService:NftserService) { 
    this.menuopt = [
      {name: 'Transaction History', code: 'TRH'},
      {name: 'Home', code: 'HM',},
      {name: 'Own NFT', code: 'OT'},
      {name: 'Wallet (Add/Withdraw)', code:'WA'}
  ];
  }

  ngOnInit(): void {
    this.homepage();
  }
  login(){
    this.router.navigate(['/login']);
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
    else if(e.value.code=='HM') {
      this.router.navigate(['/home']);
    }
  }
  walletTrans(){
    this.selectedwBtn=true;
    this.selectedNBtn=false;
  }
  nftTrans(){
    this.selectedwBtn=false;
    this.selectedNBtn=true;
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

}
