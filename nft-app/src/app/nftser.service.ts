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

  constructor(private http: HttpClient) { }
  loginApi(params:any){
    console.log("Successful");
     return this.http.post('http://localhost:4000/login',{
      'username':params.username,
      'password':params.password
     })
    
  }
}
