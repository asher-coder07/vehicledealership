import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { switchMap } from 'rxjs';
import { PartOrderFormComponent } from '../part-order-form/part-order-form.component';
import { SellVehicleFormComponent } from '../sell-vehicle-form/sell-vehicle-form.component';

@Component({
  selector: 'app-vehicle-detail',
  templateUrl: './vehicle-detail.component.html',
  styleUrls: ['./vehicle-detail.component.scss']
})
export class VehicleDetailComponent implements OnInit {

  userRole!: string;
  vin!: string | null;

  constructor(
    private ar: ActivatedRoute,
    private cookie: CookieService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.userRole = this.cookie.get('user_role');
    this.vin = this.ar.snapshot.paramMap.get('vin');
    // TODO: call to get vehicle detail by vin number
  }

  get isClerkOrOwner(): boolean {
    return ['InventoryClerk', 'Owner'].includes(this.userRole);
  }

  get isManagerOrOwner(): boolean {
    return ['Manager', 'Owner'].includes(this.userRole);
  }

  get isSalesOrOwner(): boolean {
    return ['SalesPeople', 'Owner'].includes(this.userRole);
  }

  addPartOrder(): void {
    if (!this.isClerkOrOwner) {
      alert('no permission to add part order');
      return;
    }
    const dialogRef = this.dialog.open(PartOrderFormComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log('result of part order dialog', result);
    });
  }

  sellVehicle(): void {
    if (!this.isSalesOrOwner) {
      alert('no permission to sell');
      return;
    }
    const dialogRef = this.dialog.open(SellVehicleFormComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log('result of sell vehicle dialog', result);
    });

  }



}
