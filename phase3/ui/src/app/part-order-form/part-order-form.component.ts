import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-part-order-form',
  templateUrl: './part-order-form.component.html',
  styleUrls: ['./part-order-form.component.scss']
})
export class PartOrderFormComponent {
  addPartOrderForm: FormGroup;
  addPartForm: FormGroup;
  showAddPartFormBool = false;
  partsAdded: Array<any> = []
  partStatus = ['ordered', 'received', 'installed']

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private cookie: CookieService,
    private router: Router,
    private api: ApiService
  ){
    this.addPartOrderForm = this.fb.group({
      vendor: this.fb.control(''),
      total_cost: this.fb.control('')
    })

    this.addPartForm = this.fb.group({
      part_number: this.fb.control(''),
      description: this.fb.control(''),
      cost: this.fb.control(''),
      quantity: this.fb.control(''),
      status: this.fb.control('')
    })



  }
  showAddPartForm(): void {
    this.showAddPartFormBool = true
  }

  savePart(): void {
    console.log('Save part button', this.addPartForm.value)
    let data: object = this.addPartForm.value
    this.partsAdded.push(data)
    let partsCost: number = this.partsAdded.map(a => a.cost).reduce((acc, val)=> acc+val)
    this.addPartOrderForm.patchValue({
      total_cost: partsCost
    })
    console.log('Array of parts', this.partsAdded)
    this.addPartForm.reset()
  }

  savePartOrder(): void {
    let body = this.addPartOrderForm.value
    body['parts'] = this.partsAdded
    // Add VIN from previous menu selection
    body['vin'] = this.cookie.get('vin')
    // Add username from session info or cookies
    body['username'] = this.cookie.get('username')

    console.log('Request body for add part order', body)
    this.http.post('http://localhost:5000/part/order', body).subscribe({
      next: (result: any) => {
        console.log('saved sale', result)

      },
      error: (err) => {
        console.log(err)
      }
    })
  }

}