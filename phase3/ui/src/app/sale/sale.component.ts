import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatListOption } from '@angular/material/list';

@Component({
  selector: 'app-sale',
  templateUrl: './sale.component.html',
  styleUrls: ['./sale.component.scss']
})
export class SaleComponent {

  addSaleForm: FormGroup;
  customerSearchForm: FormGroup;

  displayedColumns: string[] = [];
  customerSearchData = []
  customers = [] 

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private cookie: CookieService,
    private router: Router,
    private api: ApiService
  ) {
    this.customerSearchForm = this.fb.group({
      id: this.fb.control(''),
      phone: this.fb.control(''),
      name: this.fb.control('')
    })

    this.addSaleForm = this.fb.group({
      buyer: this.fb.control(''),
      // vin: this.fb.control(''),
      date: this.fb.control('')
    });

  }
  searchCustomer(): void {
    this.api.search_customers(this.customerSearchForm.value).subscribe({
      next: (res) => {
        console.log(res)
        this.displayedColumns = res['metadata']
        this.customerSearchData = res['data']

      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  onSelectCustomer(options: MatListOption[]): void {
    let selected = options.map(o => o.value)
    console.log('Selected customer', selected)
    this.addSaleForm.patchValue({
      buyer: selected[0].id
    })
  }

  save(): void {
    let data = this.addSaleForm.value
    let username = this.cookie.get('username')
    // VIN selected from inventory page
    let vin = this.cookie.get('vin')
    data['username'] = username
    data['vin'] = username
    console.log('customer selected', this.customers)

    // Calculate the seling price and parts costs
    this.http.get('http://localhost:5000/vehicle?vin='+vin).subscribe({
      next: (result: any) => {
        console.log('get vehicle '+ vin, result)
        data['price'] = result.data.price
      },
      error: (err: any) => {
        console.log(err)
      }
    })

    console.log('save sale', this.addSaleForm.value)
    this.http.post('http://localhost:5000/sale', this.addSaleForm.value).subscribe({
      next: (result: any) => {
        console.log('saved sale', result)

      },
      error: (err) => {
        console.log(err)
      }
    })
  }


}
