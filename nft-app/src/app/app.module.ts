import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {CardModule} from 'primeng/card';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import {PasswordModule} from 'primeng/password';
import {ButtonModule} from 'primeng/button';
import { HomeComponent } from './home/home.component';
import {DropdownModule} from 'primeng/dropdown';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {TableModule} from 'primeng/table';
import {OverlayPanelModule} from 'primeng/overlaypanel';
import {DialogModule} from 'primeng/dialog';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import {ToastModule} from 'primeng/toast';
import { OwnNftComponent } from './own-nft/own-nft.component';
import { AddTowalletComponent } from './add-towallet/add-towallet.component';
import {RadioButtonModule} from 'primeng/radiobutton';
import { TransHistoryComponent } from './trans-history/trans-history.component';
import {SidebarModule} from 'primeng/sidebar';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignUpComponent,
    HomeComponent,
    OwnNftComponent,
    AddTowalletComponent,
    TransHistoryComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    AppRoutingModule,
    CardModule,
    PasswordModule,
    ButtonModule,
    DropdownModule,
    TableModule,
    OverlayPanelModule,
    DialogModule,
    HttpClientModule,
    RadioButtonModule,
    FormsModule,
    ToastModule,
    ReactiveFormsModule,
    SidebarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
