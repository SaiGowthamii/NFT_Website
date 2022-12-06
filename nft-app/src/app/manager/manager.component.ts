import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NftserService } from '../nftser.service';
import * as _moment from 'moment';
import { DatePipe } from '@angular/common';
@Component({
  selector: 'app-manager',
  templateUrl: './manager.component.html',
  styleUrls: ['./manager.component.scss']
})
export class ManagerComponent implements OnInit {
  
  result:any[]=[];
  userDetails:any=[];
  display:boolean=false;
  selectedwBtn:boolean=true;
  selectedNBtn:boolean=false;
  selectedABtn:boolean=false;
  side_bar:boolean=true;
  showData:boolean=false;
  showLoader:boolean=false;
  cancelText:any='';
  selected:any;
  log_time:any={};
  create_res:any=[]
  first_name:any='';
  last_name:any='';
  level_manager:number | undefined;
  username:any=''
  password:any=''
  minDateValue=new Date();
  rangeDates: Date[]=[];
  enterDetails:boolean=false;
  addenterDetails:boolean=false
  errormessage:string="Please fill all the fields"
  name:any=localStorage.getItem('fname');
  level:any=localStorage.getItem('trader_level');
  balance:any=localStorage.getItem('wallet_balance');
  cancelledTransactions:any='';
  successfulTransactions:any='';
  totalAddedWalletAmountinETH:any='';
  totalAddedWalletAmountinUSD:any='';
  buyTransactions:any='';
  totalAdds:any='';
  totalAmountInEth:any='';
  totalNFTTransactions:any='';
  totalTransactions:any='';
  totalWalletTransaction:any='';
  totalWithdrawnWalletAmountinETH:any='';
  totalWithdrawnWalletAmountinUSD:any='';
  totalwithdraws:any='';
  visiblecreate:boolean=false;
  nftName:any='';
  ethAdd:any='';
  ownerId:any='';
  current_price:any='';
  tkId:any='';
  sellTransactions:any='';

  constructor(private router:Router,private nftService:NftserService) {
    
   }

  ngOnInit(): void {
    if(this.level==3){
      this.visiblecreate=true;
    }
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
  create_manager(){
    this.selectedwBtn=false;
    this.selectedNBtn=true;
    this.selectedABtn=false;
    this.display=false;
  }
  report(){
    this.selectedwBtn=true;
    this.selectedNBtn=false;
    this.selectedABtn=false;
  }
  add_nft(){
  this.selectedABtn=true;
  this.selectedwBtn=false;
  this.selectedNBtn=false;
  this.display=false;


  }
  homepage(){
    if(this.username==''||this.password==''||this.last_name==''||this.first_name==''||this.level==undefined){
      this.enterDetails=true;
    }
    else{
      let user:any={}
      let t_id=localStorage.getItem('t_id')
      user={
        "manager_username":this.username,
        "manager_password":this.password,
        "manager_fname":this.first_name,
        "manager_lname":this.last_name,
        "manager_level":this.level_manager,
        "initiator_id": t_id
      }
      console.log("user",user)
      this.nftService.managerApi(user).subscribe(data=>{
        console.log('data',data);
        this.create_res=data;
        if(this.create_res.res=="success"){
          alert(this.create_res.message)
        }
        else{
          this.enterDetails=true;
          this.errormessage=this.create_res.message;
          
        }
       
        // this.router.navigate(['/login']);
        
      },error => {
        // You can access status:
        console.log(error.status);
        alert("Session has expired")
      this.login();})

    }
   }
   reset_cal(){
    this.rangeDates=[];
   }

   onfocus(){
    this.enterDetails=false;
   
  }

  report_details(){
    let start= new DatePipe('en-Us').transform(this.rangeDates[0], 'yyyy-MM-dd', 'IST')
    let end= new DatePipe('en-Us').transform(this.rangeDates[1], 'yyyy-MM-dd', 'IST')
    console.log("end",end)
    if(start==null || end==null){
      alert('Select the Date Range');
    }
    else{
    let tid=localStorage.getItem('t_id');
    let params={
      "from_date":start,
      "to_date":end,
      "initiator_id":tid }
      this.nftService.report_get(params).subscribe(data=>{
        this.display=true;
        let result:any=[];
        result=data;
        this.cancelledTransactions=result.cancelledTransactions
        this.successfulTransactions=result.successfulTransactions;
        this.totalAddedWalletAmountinETH=result.totalAddedWalletAmountinETH;
        this.totalAddedWalletAmountinUSD=result.totalAddedWalletAmountinUSD;
        this.totalAdds=result.totalAdds; 
        this.totalAmountInEth=result.totalAmountInEth;
        this.totalNFTTransactions=result.totalNFTTransactions;
        this.totalTransactions=result.totalTransactions;
        this.totalWalletTransaction=result.totalWalletTransaction;
        this.totalWithdrawnWalletAmountinETH=result.totalWithdrawnWalletAmountinETH;
        this.totalWithdrawnWalletAmountinUSD=result.totalWithdrawnWalletAmountinUSD;
        this.totalwithdraws=result.totalwithdraws;
        this.buyTransactions=result.buyTransactions;
        this.sellTransactions=result.sellTransactions;
        
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


   cancel(){
    this.display=true;
   }
    addNft(){
      if(this.nftName==''||this.ethAdd==''||this.tkId==''||this.ownerId==''||this.current_price==''){
        this.addenterDetails=true;
      }
      else{
        let user:any={}
        let t_id=localStorage.getItem('t_id')
        user={
          "nft_name":this.nftName,
          "contract_addr":this.ethAdd,
          "token_id":this.tkId,
          "owner_id":this.ownerId,
          "current_price":this.current_price,
          "initiator_id":t_id
        }
        console.log("user",user)
        this.nftService.addNftApi(user).subscribe(data=>{
          this.create_res=data;
          if(this.create_res.res=="success"){
            alert(this.create_res.message)  
            this.nftName='';
            this.ethAdd='';
            this.tkId='';
            this.ownerId='';
            this.current_price=''
          }
          else{
            this.addenterDetails=true;
            this.errormessage=this.create_res.message;
            
          }
         
          // this.router.navigate(['/login']);
          
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
         
         console.log("NFT",this.nftName)
  
      }
     }

}
