import { Component, OnInit } from '@angular/core';
import {NftserService} from '../nftser.service';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-add-towallet',
  templateUrl: './add-towallet.component.html',
  styleUrls: ['./add-towallet.component.scss']
})
export class AddTowalletComponent implements OnInit {
  menuopt: any[] ;
  ethadd:any;
  token_id:any;
  selectedCity:any;
  sales: any=[];
  result:any[]=[];
  userDetails:any=[];
  paymentDetails:any=[];
  display:boolean=false;
  showData:boolean=false;
  showLoader:boolean=false;
  selected:any;
  accNo:any='';
  amount:any='';
  usdAmount:any;
  showusd:boolean=false;
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  selectedValue: string = 'add';
  validboolean:boolean=false;

  constructor(private router:Router,private nftService:NftserService) {
    this.homepage();
    this.menuopt = [
      {name: 'Wallet (Add/Withdraw)', code:'WA'},
      {name: 'Home', code: 'HM',},
      {name: 'Own NFT', code: 'OT'},
      {name: 'Transaction History', code: 'TRH'},
      
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
  onfocusamount(){
    this.validboolean=false;
  }
  onfocusIn(){
    this.showusd=false;
    this.validboolean=false;
  }
  homepage(){
   this.userDetails=localStorage.getItem('t_id');
   console.log(this.userDetails);
   this.showLoader=true;
    this.nftService.homeApi(this.userDetails).subscribe(data=>{
      this.showLoader=false;
      if(data.res=='failed'){
        alert(data.res);
      }
      else{
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
        }
      
       });

  }
  reset(){
   this.ethadd=null;
   this.token_id=null;
   this.homepage();
  }
  onChange(e:any){
    console.log("Event",e);
    if(e.value.code=='OT') {
      this.router.navigate(['/own']);
    }else if(e.value.code=='HM') {
      this.router.navigate(['/home']);
    }
    else if(e.value.code=='WA') {
      this.router.navigate(['/addTowallet']);
    }
    else if(e.value.code=='TRH') {
      this.router.navigate(['/history']);
    }
  }

  conversion(){
    if(this.amount!=''){
      this.nftService.amountConversion(this.amount).subscribe(data=>{
          this.usdAmount=data.amountUSD;
          this.showusd=true;
          console.log("The amountt",this.usdAmount);
      })
    }
    else{
      alert('Enter the amount');
    }
  }
  
  submit(){
    if(this.accNo!=''&& this.amount!=''){
    console.log("change",this.usdAmount);
    let id=localStorage.getItem('t_id');
    this.paymentDetails={
      "initiator_id":id,
      "amount_in_eth":this.amount,
      "payment_addr":this.accNo,
      "type":this.selectedValue,

    }
    this.showLoader=true;
     this.nftService.walletApi(this.paymentDetails).subscribe(data=>{
     let result:any
     result=data;
     console.log('res',result.updated_balance)
     if(result.res=='success'){
      this.balance=result.updated_balance;
      localStorage.setItem('wallet_balance',this.balance);
      alert('Transaction Successfull');
      this.reset_window();
     }
     else{
      alert(result.message);
      this.reset_window();
      
     }
       
    });
  }
  else{
    this.validboolean=true;
  }
  }
  reset_window(){
    this.accNo='';
    this.amount='';
    this.showusd=false;
    this.selectedValue='add';

  }

  

}
