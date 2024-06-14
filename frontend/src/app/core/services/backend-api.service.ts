import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Usuario } from '../models/usuario';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private baseUrl = 'http://127.0.0.1:8000/backend_app/' 

  constructor(private http: HttpClient) {
  }

  informacionUsuario() {
    const email = localStorage.getItem('email')

    const headers = new HttpHeaders ({
      'Content-Type': 'application/json'
    })

    return this.http.get<any>(this.baseUrl + 'usuarios/perfil/' + email, {headers} )
  }

}
