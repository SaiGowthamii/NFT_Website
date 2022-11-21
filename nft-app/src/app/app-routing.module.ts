import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { HomeComponent } from './home/home.component';
import { OwnNftComponent } from './own-nft/own-nft.component';

const routes: Routes = [
  {path: 'login', component:LoginComponent },
  {path: '', component:LoginComponent },
  {path: 'signUp', component:SignUpComponent},
  {path: 'home', component:HomeComponent},
  {path: 'own', component:OwnNftComponent}

];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
