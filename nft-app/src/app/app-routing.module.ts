import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { HomeComponent } from './home/home.component';
import { OwnNftComponent } from './own-nft/own-nft.component';
import { AddTowalletComponent } from './add-towallet/add-towallet.component';
import { TransHistoryComponent } from './trans-history/trans-history.component';
import { PaymentComponent } from './payment/payment.component';
import { SellComponent } from './sell/sell.component';

const routes: Routes = [
  {path: 'login', component:LoginComponent },
  {path: '', component:LoginComponent },
  {path: 'signUp', component:SignUpComponent},
  {path: 'home', component:HomeComponent},
  {path: 'own', component:OwnNftComponent},
  {path:'addTowallet',component:AddTowalletComponent},
  {path:'history',component:TransHistoryComponent},
  {path:'payment', component:PaymentComponent},
  {path:'sell',component:SellComponent}

];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
