import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({providedIn: 'root'}) // Eliminar providedIn
export class RegistroService {
  private baseUrl = 'http://127.0.0.1:8000/usuarios/registrar/';

  constructor(private http: HttpClient) { } // Inyección opcional

  registrarCliente(usuarioData: any, csrfToken: string): Observable<any> {
    const url = this.baseUrl + 'usuarios/registrar/';
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken // Aquí incluyes el token CSRF en los encabezados de la solicitud
    });
    return this.http.post<any>(url, usuarioData, { headers });
  }
}
