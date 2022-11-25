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
  userName:any=localStorage.getItem('username');
  passWord:any|undefined;
  user:any={}
  eth:any|undefined;
  td:any|undefined;
  data_result:any=[];
  buy_data:any=[];
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
  buy(eth:any,tid:any){
    this.td=tid;
    this.eth=eth;
    localStorage.setItem("row_eth",eth);
    localStorage.setItem("row_tid",tid);
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
  submit(){
    if(this.userName=="" || this.passWord=="") {
      console.log("Nothing");
    }
    else{
      this.user={
        "username":this.userName,
        "password":this.passWord
      }
      this.nftService.loginApi(this.user).subscribe(data=>{
        console.log('data',data);
        this.data_result=data;
        if(this.data_result.res=='success'){
          let eth=this.eth;
          let tk=this.td;
          let tid=localStorage.getItem('t_id');
          let params={
            "trader_id":tid,
            "contract_addr":eth,
            "token_id":tk }
          this.nftService.buy_get(params).subscribe(data=>{
            this.buy_data=data;
            if(this.buy_data=='success'){
              this.router.navigate(['/payment']);
            }
            else{
              alert('You dont have Sufficient Balance');
              this.display=false;
            }
          }) 
        }
        else{
          alert('Enter Correct Password');
          this.passWord='';
        }
      })
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
