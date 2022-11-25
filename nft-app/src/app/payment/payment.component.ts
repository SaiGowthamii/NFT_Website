import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NftserService } from '../nftser.service';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss']
})
export class PaymentComponent implements OnInit {
  ethadd:any;
  token_id:any;
  selectedCity:any;
  buy_data: any=[];
  nft_name:any;
  nft_add:any;
  nft_tk:any;
  nft_price:any;
  display:boolean=false;
  showData:boolean=false;
  showLoader:boolean=false;
  selected:any;
  accNo:any;
  amount:any='';
  usdAmount:any;
  ethAmount:any;
  showusd:boolean=false;
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  selectedValue: string = 'add';
  display_usd:boolean=false;
  display_eth:boolean=true;

  constructor(private router:Router,private nftService:NftserService) { 
    
  }

  ngOnInit(): void {
    this.submit();
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

  fiat(){
    this.display_usd=true;
    this.display_eth=false;
  }
  etherum(){
    this.display_eth=true;
    this.display_usd=false;
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
  submit(){
          let eth=localStorage.getItem('row_eth');
          let tk=localStorage.getItem('row_tid');
          let tid=localStorage.getItem('t_id');
          let params={
            "trader_id":tid,
            "contract_addr":eth,
            "token_id":tk }
          this.nftService.buy_get(params).subscribe(data=>{
            console.log("data",data)
            this.buy_data=data;
            if(this.buy_data.res=='successful'){
             this.nft_name=this.buy_data.nft_name;
             this.nft_add=this.buy_data.contract_addr; 
             this.nft_tk=this.buy_data.token_id;
             this.nft_price=this.buy_data.current_price;

             this.usdAmount=this.buy_data.commission_in_usd;
             this.ethAmount=this.buy_data.commission_in_eth;
            }
            else{
              alert('You dont have Sufficient Balance');
              this.display=false;
            }
          }) 

  }
  proceed(){
    let type:any;
    if(this.display_eth==true){
      type='eth'
    }
    else{
      type='fiat'
    }
    let eth=localStorage.getItem('row_eth');
          let tk=localStorage.getItem('row_tid');
          let tid=localStorage.getItem('t_id');
          let params={
            "trader_id":tid,
            "contract_addr":eth,
            "token_id":tk,
          "commission_type":type }
    this.nftService.buy_post(params).subscribe(data=>{
      let result:any=[];
      result=data;
      if(result.res=='successful')
      {
        alert(result.message);
      }
      else{
        alert(result.message);
      }
      this.router.navigate(['/home']);
      
    })
  }

}
