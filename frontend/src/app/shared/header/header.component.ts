import { Component, OnInit } from '@angular/core';
import { AuthService, Online } from '../../core/services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Observable, Subscription, tap } from 'rxjs';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  imports: [CommonModule],
  standalone: true,
})
export class HeaderComponent implements OnInit {
  public isOnline: boolean | undefined; 
  public email: string | null | undefined;
  private dataSubscription: Subscription | undefined;

  constructor(private authAPI: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.dataSubscription = this.authAPI.authObservable
      .pipe(
        tap((data) => {
          this.isOnline = data.isOnline; 
          console.log('isOnline:', this.isOnline); 
        })
      )
      .subscribe();
  }

  logout(): void {
    this.authAPI.logOutCliente().subscribe({
      next: (response: any) => {
        console.log(response);
        this.router.navigate(['']);
      },
      error: (error: any) => {
        console.error(error);
      },
    });
  }

  navigateToProfile(): void {
    this.router.navigate(['pages/profile/']);
  }

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }
}
