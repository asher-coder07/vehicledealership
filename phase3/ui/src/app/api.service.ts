import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  api = 'http://localhost:5000';

  constructor(
    private http: HttpClient
  ) { }

  get_vehicle_manufacturers(): Observable<any> {
    const url = `${this.api}/manufacturer/`;
    return this.http.get(url);
  }

  get_vehicle_vendors(): Observable<any> {
    const url = `${this.api}/vendor/`;
    return this.http.get(url);
  }

  get_vehicle_types(): Observable<any> {
    const url = `${this.api}/vehicle-type/`;
    return this.http.get(url);
  }

  search_vehicle(params: any): Observable<any> {
    const url = `${this.api}/vehicle`;

    return this.http.get(url, { params });
  }

  search_customers(params: any): Observable<any>{
    const url = `${this.api}/customer/search`;
    return this.http.get(url, { params });
  }

  search_vendors(params: any): Observable<any>{
    const url = `${this.api}/vendor`;
    return this.http.get(url, { params });
  }

}
