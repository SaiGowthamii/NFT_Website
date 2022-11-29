import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class NftserService {

 url='http://localhost:4000/getNFTDataForHome';
 ownNft='http://localhost:4000/getNFTDataForTrader';
 conversion='http://localhost:4000/convertETH';
 history='http://localhost:4000/getTransactionHistory'

  constructor(private http: HttpClient) { }
  loginApi(params:any){
    console.log("Successful");
     return this.http.post('http://localhost:4000/login',{
      'username':params.username,
      'password':params.password
     })
    
  }
  SignupApi(params:any){
     return this.http.post('http://localhost:4000/signUp',{
      "first_name":params.first_name,
      "last_name":params.last_name,
      "eth_address":params.eth_address,
      "email":params.email,
      "cell_no":params.cell_no,
      "ph_no":params.ph_no,
      "street_addr":params.street_addr,
      "city":params.city,
      "state":params.state,
      "zip":params.zip,
      "username":params.username,
      "password":params.password
     })
  }
    public homeApi(id :any) : Observable<any>{ 
      let token=localStorage.getItem("token");
      let headers = { 'content-type': 'application/json',
      'Authorization': `Bearer ${token}`} 
     
      const requestOptions = { headers: headers };
      return this.http.get(this.url + '?trader_id=' + id,requestOptions);
  }
  public ownNftApi(id :any) : Observable<any>{  
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    const requestOptions = { headers: headers };
    return this.http.get(this.ownNft + '?trader_id=' + id,requestOptions);
  }
  public amountConversion(id :any) : Observable<any>{  
    return this.http.get(this.conversion + '?amount_in_eth=' + id);
  }
  walletApi(params:any){
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
     return this.http.post('http://localhost:4000/modifyWallet',{
        "initiator_id":params.initiator_id,
        "amount_in_eth":params.amount_in_eth,
        "wallet_trans_type":params.type,
        "payment_addr":params.payment_addr,
        
     },{ headers: headers })
  }
  
  buy_get(params:any){
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    let queryParams = new HttpParams();
   queryParams = queryParams.append("trader_id",params.trader_id);
   queryParams = queryParams.append("contract_addr",params.contract_addr);
   queryParams = queryParams.append("token_id",params.token_id);
    return this.http.get('http://localhost:4000/buyNFT',{params:queryParams,headers: headers},)
  }
  buy_post(params:any) {
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    return this.http.post('http://localhost:4000/buyNFT',{
        "trader_id":params.trader_id,
        "contract_addr":params.contract_addr,
        "token_id":params.token_id,
        "commission_type":params.commission_type    
     },{ headers: headers })
  }
  sell_get(params:any){
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    let queryParams = new HttpParams();
   queryParams = queryParams.append("trader_id",params.trader_id);
   queryParams = queryParams.append("contract_addr",params.contract_addr);
   queryParams = queryParams.append("token_id",params.token_id);
    return this.http.get('http://localhost:4000/sellNFT',{params:queryParams,headers: headers})
  }
  sell_post(params:any) {
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    return this.http.post('http://localhost:4000/sellNFT',{
      "trader_id":params.trader_id,
      "contract_addr":params.contract_addr,
      "token_id":params.token_id,
      "receiver_eth_addr":params.receiver_eth_addr,
      "commission_type":params.commission_type   
     },{ headers:headers })
  }
  public historyApi(id :any) : Observable<any>{  
    let token=localStorage.getItem("token");
    let headers = { 'content-type': 'application/json',
    'Authorization': `Bearer ${token}`} 
    const requestOptions = { headers: headers };
    return this.http.get(this.history + '?trader_id=' + id,requestOptions);
}
public cancelApi(params:any){
  let token=localStorage.getItem("token");
  let headers = { 'content-type': 'application/json',
  'Authorization': `Bearer ${token}`} 
  return this.http.post('http://localhost:4000/cancelNFTTransaction',{
    "trans_id":params.trans_id,
    "log_info":params.log_info,
    "time_stamp": params.time_stamp
     },{ headers: headers })

}
managerApi(params:any){
  let token=localStorage.getItem("token");
  let headers = { 'content-type': 'application/json',
  'Authorization': `Bearer ${token}`} 
  return this.http.post('http://localhost:4000/createManager',{
    "manager_username":params.manager_username,
    "manager_password":params.manager_password,
    "manager_fname":params.manager_fname,
    "manager_lname":params.manager_lname,
    "manager_level":params.manager_level,
    "initiator_id":params.initiator_id
  },{ headers: headers })
}
addNftApi(params:any){
  let token=localStorage.getItem("token");
  let headers = { 'content-type': 'application/json',
  'Authorization': `Bearer ${token}`} 
  return this.http.post('http://localhost:4000/addNFT',{
    "nft_name":params.nft_name,
    "contract_addr":params.contract_addr,
    "token_id":params.token_id,
    "owner_id":params.owner_id,
    "current_price":params.current_price,
    "initiator_id":params.initiator_id
  },{ headers: headers })
}
report_get(params:any){
  let token=localStorage.getItem("token");
  let headers = { 'content-type': 'application/json',
  'Authorization': `Bearer ${token}`} 
  let queryParams = new HttpParams();
  console.log(params);
 queryParams = queryParams.append("from_date",params.from_date);
 queryParams = queryParams.append("to_date",params.to_date);
 queryParams = queryParams.append("initiator_id",params.initiator_id);
  return this.http.get('http://localhost:4000/getReports',{params:queryParams,headers: headers})
}
}
