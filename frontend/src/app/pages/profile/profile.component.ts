import { Component } from '@angular/core';
import { BackendApiService } from '../../core/services/backend-api.service';
import { Usuario } from '../../core/models/usuario';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { Subscription, tap } from 'rxjs';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css',
})
export class ProfileComponent {
  usuario: Usuario = {
    nombre: '',
    apellido: '',
    email: '',
    contrasenia: '',
    telefono: '',
    direccion: '',
  };

  public isOnline: boolean | undefined;
  public email: string | null | undefined;
  private dataSubscription: Subscription | undefined;

  constructor(
    private backendService: BackendApiService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.dataSubscription = this.authService.authObservable
      .pipe(
        tap((data) => {
          this.isOnline = data.isOnline;
          console.log('isOnline:', this.isOnline);
        })
      )
      .subscribe();

    if (this.isOnline == false) {
      return
    }  else {
      this.obtenerInformacion()
    }
  }

  obtenerInformacion() {
    this.backendService.informacionUsuario().subscribe({
      next: (data) => {
        this.usuario = {
          nombre: data.nombre,
          apellido: data.apellido,
          email: data.email,
          telefono: data.telefono,
          direccion: data.direccion,
        };

        console.log('informacion de usuario', data);
        return this.usuario;
      },
      error: (error) => {
        console.log('error al traer informacion', error);
      },
    });
  }
}
