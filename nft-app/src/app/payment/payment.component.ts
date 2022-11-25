import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NftserService } from '../nftser.service';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss']
})
export class PaymentComponent implements OnInit {
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
  accNo:any;
  amount:any='';
  usdAmount:any;
  showusd:boolean=false;
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  selectedValue: string = 'add';

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
    this.showusd=false;
  }
  onfocusIn(){
    this.showusd=false;
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
          this.sales=[];
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
     }
     else{
      alert('Transcation Failed');
     }
       
    });

  }

}
