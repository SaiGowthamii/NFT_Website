import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import {NftserService} from '../nftser.service';

@Component({
  selector: 'app-own-nft',
  templateUrl: './own-nft.component.html',
  styleUrls: ['./own-nft.component.scss']
})
export class OwnNftComponent implements OnInit {
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
  constructor(private router:Router,private nftService:NftserService) { 
    this.homepage();
    this.menuopt = [
      {name: 'Own NFT', code: 'OT'},
      {name: 'Home', code: 'HM',},
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
  homepage(){
  //  this.userDetails=localStorage.getItem('t_id');
  //  console.log(this.userDetails);
  //  this.showLoader=true;
  //   this.nftService.homeApi(this.userDetails).subscribe(data=>{
  //     this.showLoader=false;
  //        for(let i in data){
  //         let temp={
  //               'nft_name':data[i].nft_name,
  //               'contract_addr':data[i].contract_addr,
  //               'token_id' :data[i].token_id,
  //               'current_price':data[i].current_price
  //             }
  //             this.sales.push(temp);
  //        }
  //     console.log(this.sales)
      
  //      });

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
  }

}
