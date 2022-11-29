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
  history: any=[];
  result:any[]=[];
  userDetails:any=[];
  display:boolean=false;
  selectedwBtn:boolean=true;
  selectedNBtn:boolean=false;
  side_bar:boolean=true;
  showData:boolean=false;
  showLoader:boolean=false;
  cancelText:any='';
  selected:any;
  log_time:any={};
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
    this.homepage();
  }
  nftTrans(){
    this.selectedwBtn=false;
    this.selectedNBtn=true;
    this.homepage();
  }
  homepage(){
    this.userDetails=localStorage.getItem('t_id');
    console.log(this.userDetails);
    this.showLoader=true;
    this.sales=[];
    this.history=[];
     this.nftService.historyApi(this.userDetails).subscribe(data=>{
       this.showLoader=false;
       let result:any=[]
       result=data;
       if(result.length!=0){
          for(let i in data){
            if(data[i].trans_type=='wallet') {
              let temp={
                "trans_id": data[i].trans_id,
                 "wallet_trans_type": data[i].wallet_trans_type,
                 "amount_in_eth": data[i].amount_in_eth,
                 "amount_in_usd": data[i].amount_in_usd,
                 "payment_addr": data[i].payment_addr,
                 "trans_dateTime": data[i].trans_dateTime
              }
              this.sales.push(temp);
            }
            else{
              let temp={
                "trans_id": data[i].trans_id,
                "contract_addr":  data[i].contract_addr,
                "token_id": data[i].token_id,
                "total_amount": data[i].total_amount,
                "commission_in_eth": data[i].commission_in_eth,
                "commission_in_usd": data[i].commission_in_usd,
                "commission_type": data[i].commission_type,
                "nft_trans_type": data[i].nft_trans_type,
                "trans_status": data[i].trans_status,
                "trans_dateTime": data[i].trans_dateTime
              }
              this.history.push(temp);

            }    
          }
        }
        },error => {
          // You can access status:
          console.log(error.status);
          if(error.status==401){
            alert("Session has expired")
            this.login();
          }
          else{
            alert(error.message);
          }
         });
        if(this.sales.length==0){
          this.sales=[];
        }
        if(this.history.length==0){
          this.history=[];
        }
 
   }

   cancel(){
    this.display=true;
   }
   submit(){
    if(this.cancelText=='') {
      alert("Please Do Enter The Reason");
    }
    else{
    this.userDetails=localStorage.getItem('t_id');
    this.log_time={
      "trans_id":this.userDetails,
      "log_info":this.cancelText,
      "time_stamp": Date.now() }
      this.nftService.cancelApi(this.log_time).subscribe(data=>{
        let cancel_res:any=[];
        cancel_res=data;
        if(cancel_res.res=='success'){
          alert('Transaction Cancelled Successfull');
          this.homepage();
          this.display=false;
        }
        else{
          alert(cancel_res.message);
          this.homepage();
          this.display=false;
        }
      },error => {
        // You can access status:
        console.log(error.status);
        if(error.status==401){
          alert("Session has expired")
          this.login();
        }
        else{
          alert(error.message);
        }
       })
    }
    }
  }



