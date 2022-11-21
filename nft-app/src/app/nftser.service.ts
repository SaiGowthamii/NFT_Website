import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class NftserService {
 headers = { 'content-type': 'application/json'}
 url='http://localhost:4000/getNFTDataForHome';
  constructor(private http: HttpClient) { }
  loginApi(params:any){
    console.log("Successful");
     return this.http.post('http://localhost:4000/login',{
      'username':params.username,
      'password':params.password
     })
    
  }
  SignupApi(params:any){
    console.log("Successful");
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
      return this.http.get(this.url + '?trader_id=' + id);
  }
}
