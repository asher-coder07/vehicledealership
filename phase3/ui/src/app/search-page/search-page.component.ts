import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { ApiService } from '../api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent implements OnInit, AfterViewInit {

  userRole: string;
  publicSearchForm!: FormGroup;

  manufacturerOptions = [];
  vendorOptions = [];
  vehicleTypeOptions = [];
  fuelTypeOptions = [
    'Battery',
    'Hybrid',
    'Fuel Cell',
    'Gas',
    'Diesel',
    'Natural Gas',
    'Plugin Hybrid'
  ];

  displayedColumns: string[] = [];
  dataSource = new MatTableDataSource<any>([]);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private cookie: CookieService,
    private fb: FormBuilder,
    private http: HttpClient,
    private api: ApiService,
    private router: Router
  ) {
    this.userRole = this.cookie.get('user_role');
  }

  get shouldDisplayVin(): boolean {
    return ['Owner', 'SalesPeople', 'InventoryClerk', 'Manager'].includes(this.userRole);
  }

  get shouldDisplayClerkCard(): boolean {
    return ['InventoryClerk', 'Owner'].includes(this.userRole);
  }

  get shouldDisplayMgrCard(): boolean {
    return ['Manager', 'Owner'].includes(this.userRole);
  }

  get shouldDisplaySalespeopleCard(): boolean {
    return ['SalesPeople', 'Owner'].includes(this.userRole);
  }

  ngOnInit(): void {
    this.publicSearchForm = this.fb.group({
      vehicleType: this.fb.control(''),
      manufacturerName: this.fb.control(''),
      fuelType: this.fb.control(''),
      modelName: this.fb.control(''),
      modelYear: this.fb.control(''),
      description: this.fb.control(''),  // keyword
      mileage: this.fb.control(''),
      price: this.fb.control(''),
      vin: this.fb.control('')
    });

    this.api.get_vehicle_manufacturers().subscribe({
      next: (res) => {
        console.log(res);
        const manufacturers = res.data.map((d: any) => d['manufacturer_name']);
        this.manufacturerOptions = manufacturers;
      }
    });

    this.api.get_vehicle_types().subscribe({
      next: (res) => {
        console.log(res);
        const types = res.data.map((t: any) => t['vehicle_type']);
        this.vehicleTypeOptions = types;
      }
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
  }

  search(): void {
    const params: any = {};

    const vehicleType = this.publicSearchForm.get('vehicleType')?.value;
    if (vehicleType) {
      params['vehicle-type'] = vehicleType;
    }
    const manufacturerName = this.publicSearchForm.get('manufacturerName')?.value;
    if (manufacturerName) {
      params['manufacturer-name'] = manufacturerName;
    }
    const fuelType = this.publicSearchForm.get('fuelType')?.value;
    if (fuelType) {
      params['fuel-type'] = fuelType;
    }
    const modelName = this.publicSearchForm.get('modelName')?.value;
    if (modelName) {
      params['model-name'] = modelName;
    }
    const modelYear = this.publicSearchForm.get('modelYear')?.value;
    if (modelYear) {
      params['model-year'] = modelYear;
    }
    const description = this.publicSearchForm.get('description')?.value;
    if (description) {
      params['kw'] = description;
    }
    const mileage = this.publicSearchForm.get('mileage')?.value;
    if (mileage) {
      params['mileage'] = mileage;
    }
    const price = this.publicSearchForm.get('price')?.value;
    if (price) {
      params['price'] = price;
    }
    const vin = this.publicSearchForm.get('vin')?.value;
    if (vin) {
      params['vin'] = vin;
    }
    
    this.api.search_vehicle(params).subscribe({
      next: (res: any) => {
        console.log('result of search', res);
        this.displayedColumns = ['actions'].concat(res['metadata']);
        this.dataSource.data = res['data'];
      }
    });
  }

  reset(): void {
    this.publicSearchForm.reset();
    this.dataSource.data = [];
  }

  onAddVehicleClick(): void {
    if (!this.shouldDisplayClerkCard) {
      alert('no permission to navigate');
      return;
    }
    this.router.navigate(['/new-vehicle']);
  }

}
