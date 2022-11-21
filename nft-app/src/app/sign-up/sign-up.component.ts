import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import {NftserService} from '../nftser.service';
import {MessageService} from 'primeng/api';
@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss'],
  providers: [MessageService]
})
export class SignUpComponent implements OnInit {
  user:any={}
  first_name:any|undefined;
  last_name:any|undefined;
  eth_address:any|undefined;
  email:any|undefined;
  cell_no:any|undefined;
  ph_no:any|undefined;
  street_addr:any|undefined
  city:any|undefined;
  state:any|undefined;
  zip:any|undefined;
  username:any|undefined;
  password:any|undefined;
  enterDetails:boolean=false;
  result:any=[];
  display:boolean=false;
  errormessage:string="Please fill all the fields"

  constructor(private router:Router,private nftService:NftserService,private messageService: MessageService) { }

  ngOnInit(): void {
  }
  submit(){
    if(this.first_name==undefined||this.last_name==undefined||this.cell_no==undefined||this.city==undefined||this.email==undefined||this.eth_address==undefined||this.ph_no==undefined||this.street_addr==undefined||this.state==undefined||this.zip==undefined||this.username==undefined||this.password==undefined){
      this.enterDetails=true;
    }else{
      this.user={
        "first_name":this.first_name,
        "last_name":this.last_name,
        "eth_address":this.eth_address,
        "email":this.email,
        "cell_no":this.cell_no,
        "ph_no":this.ph_no,
        "street_addr":this.street_addr,
        "city":this.city,
        "state":this.state,
        "zip":this.zip,
        "username":this.username,
        "password":this.password
      }
      this.nftService.SignupApi(this.user).subscribe(data=>{
        console.log('data',data);
        this.result=data;
        if(this.result.res=="success"){
          this.display=true;
        }
        else{
          this.enterDetails=true;
          this.errormessage=this.result.message;
          
        }
        this.messageService.add({key: 'myKey1', severity:'success', summary: 'Summary Text', detail: 'Detail Text'});
        // this.router.navigate(['/login']);
        
      })

    }
  }
  login(){
    this.router.navigate(['/login']);
  }
  onfocus(){
    this.enterDetails=false;
  }

}
