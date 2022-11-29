import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import {NftserService} from '../nftser.service';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  show: boolean=false;
  user:any={}
result:any=[];
userName:any|undefined;
passWord:any|undefined;
loginbol:boolean=false;
inCorrect:boolean=false;

  constructor(private router:Router,private nftService:NftserService) { }

  ngOnInit(): any {  
    localStorage.clear();   
  }
  signUp(){
    this.router.navigate(['/signUp']);

  }
  submit(){
    if(this.userName=="" || this.passWord=="") {
     this.loginbol=true;
    }
    else{
      this.user={
        "username":this.userName,
        "password":this.passWord
      }
      this.nftService.loginApi(this.user).subscribe(data=>{
        console.log('data',data);
        this.result=data;
         console.log("login",this.result)
        if(this.result.res=='success'){
          if(this.result.user_type=='0'){
          console.log("success");
          localStorage.setItem('t_id', this.result.t_id);
          localStorage.setItem('fname', this.result.fname);
          localStorage.setItem('lname', this.result.lname);
          localStorage.setItem('trader_level', this.result.trader_level);
          localStorage.setItem('wallet_balance', this.result.wallet_balance);
          localStorage.setItem('username',this.result.username);
          localStorage.setItem('token',this.result.token);
          this.router.navigate(['/home']);
          }
          else{
            localStorage.setItem('t_id', this.result.t_id);
          localStorage.setItem('fname', this.result.fname);
          localStorage.setItem('lname', this.result.lname);
          localStorage.setItem('trader_level', this.result.manager_level);
          localStorage.setItem('username',this.result.username);
          localStorage.setItem('token',this.result.token);
          this.router.navigate(['/manager']);

          }
        }
        else{
          this.inCorrect=true;
        }
        console.log("result",this.result.res);
      })
    }
  }
  oninput(){
    this.loginbol=false;
    this.inCorrect=false;
  }
  passwordshow() {
    this.show = !this.show;
  }
  onfocus(){
    this.inCorrect=false;
    this.loginbol=false;
  }

}
