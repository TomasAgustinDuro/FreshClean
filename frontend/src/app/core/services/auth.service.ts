import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Usuario } from '../models/usuario';

export interface Online {
  isOnline: boolean;
  email: string | null;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000/backend_app/usuarios/';

  private authObservablePrivate: BehaviorSubject<Online> =
    new BehaviorSubject<Online>({
      isOnline: JSON.parse(localStorage.getItem('isOnline') || 'false'),
      email: localStorage.getItem('email') || null, 
    });

  get authObservable() {
    return this.authObservablePrivate.asObservable();
  }

  set authObservableData(data: Online) {
    this.authObservablePrivate.next(data);
  }

  constructor(private http: HttpClient) {}

  registrarCliente(usuario: Usuario): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.http.post<any>(this.baseUrl + 'registrar/', usuario, {
      headers,
    });
  }

  loginCliente(email: string, contrasenia: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    const body = { email, contrasenia };

    return this.http
      .post<any>(this.baseUrl + 'iniciar_sesion/', body, { headers })
      .pipe(
        tap((response) => {
          console.log(response)
          localStorage.setItem('email', email);
          localStorage.setItem('isOnline', 'true')
          this.authObservablePrivate.next({ isOnline: true, email: email });
        })
      );
  }

  logOutCliente(): Observable<any> {
    const email = localStorage.getItem('email')

    return this.http.post<any>(this.baseUrl + 'cerrar_sesion', { email }).pipe(
      tap((response) => {
        console.log(response);
        localStorage.setItem('isOnline', 'false');
        this.authObservablePrivate.next({
          isOnline: false,
          email: email ,
        });
      })
    );
  }
}
