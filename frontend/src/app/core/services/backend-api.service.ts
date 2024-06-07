import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Usuario } from '../models/usuario'; // Ajusta la ruta si es necesario

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private baseUrl = 'http://127.0.0.1:8000/usuarios/registrar/';

  constructor(private http: HttpClient) {}

  registrarCliente(usuario: Usuario): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.http.post<any>(this.baseUrl, usuario, { headers });
  }


private baseUrl2 = 'http://127.0.0.1:8000/usuarios/iniciar_sesion/';

  loginCliente(email: string, contrasenia: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    const body = { email, contrasenia };

    return this.http.post<any>(this.baseUrl2, body, { headers });
  }
}
