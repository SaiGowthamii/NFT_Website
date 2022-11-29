import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { NftserService } from '../nftser.service';

@Component({
  selector: 'app-own-nft',
  templateUrl: './own-nft.component.html',
  styleUrls: ['./own-nft.component.scss']
})
export class OwnNftComponent implements OnInit {
  menuopt: any[];
  ethadd: any;
  token_id: any;
  selectedCity: any;
  sales: any = [];
  result: any[] = [];
  userDetails: any = [];
  td: any = '';
  eth: any = '';
  display: boolean = false;
  showData: boolean = false;
  showLoader: boolean = false;
  sell_data: any = [];
  userName: any = localStorage.getItem('username');
  passWord: any | undefined;
  data_result: any = [];
  user = {};
  name: any = localStorage.getItem('fname');
  level: any = localStorage.getItem('trader_level');
  balance: any = localStorage.getItem('wallet_balance');
  constructor(private router: Router, private nftService: NftserService) {
    this.homepage();
    this.menuopt = [
      { name: 'Own NFT', code: 'OT' },
      { name: 'Home', code: 'HM', },
      { name: 'Transaction History', code: 'TRH' },
      { name: 'Wallet (Add/Withdraw)', code: 'WA' }
    ];
  }

  ngOnInit(): void {
  }
  login() {
    this.router.navigate(['/login']);
  }
  sell(eth: any, tid: any) {
    this.td = tid;
    this.eth = eth;
    localStorage.setItem("sell_eth", eth);
    localStorage.setItem("sell_tid", tid);
    this.display = true
  }
  homepage() {
    this.userDetails = localStorage.getItem('t_id');
    console.log(this.userDetails);
    this.showLoader = true;
    this.nftService.ownNftApi(this.userDetails).subscribe(data => {
      this.showLoader = false;
      if (data.res == 'failed') {
        alert(data.res);
      }
      else {
        for (let i in data) {
          let temp = {
            'nft_name': data[i].nft_name,
            'contract_addr': data[i].contract_addr,
            'token_id': data[i].token_id,
            'current_price': data[i].current_price
          }
          this.sales.push(temp);
        }
        console.log(this.sales)
      }

    },error => {
      // You can access status:
      console.log(error.status);
      localStorage.clear();
      alert("Session has expired")
    this.login();});

  }

  reset() {
    this.ethadd = null;
    this.token_id = null;
    this.homepage();
  }
  onChange(e: any) {
    console.log("Event", e);
    if (e.value.code == 'OT') {
      this.router.navigate(['/own']);
    } else if (e.value.code == 'HM') {
      this.router.navigate(['/home']);
    }
    else if (e.value.code == 'WA') {
      this.router.navigate(['/addTowallet']);
    }
    else if (e.value.code == 'TRH') {
      this.router.navigate(['/history']);
    }
  }
  submit() {
    if (this.userName == "" || this.passWord == "") {
      console.log("Nothing");
    }
    else {
      this.user = {
        "username": this.userName,
        "password": this.passWord
      }
      this.nftService.loginApi(this.user).subscribe(data => {
        console.log('data', data);
        this.data_result = data;
        if (this.data_result.res == 'success') {
          let eth = this.eth;
          let tk = this.td;
          let tid = localStorage.getItem('t_id');
          let params = {
            "trader_id": tid,
            "contract_addr": eth,
            "token_id": tk
          }
          this.nftService.sell_get(params).subscribe(data => {
            console.log("data", data)
            this.sell_data = data;
            if (this.sell_data.res == 'successful') {
              this.router.navigate(['/sell']);
            }
            else {
              alert(this.data_result.message);
              this.display = false;
            }
          })
        }
        else {
          alert(this.data_result.message);
          this.passWord = '';
        }
      },error => {
        // You can access status:
        console.log(error.status);
        localStorage.clear();
        alert("Session has expired")
      this.login();})
    }
  }

}
