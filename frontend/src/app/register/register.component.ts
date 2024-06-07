// register.component.ts
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { BackendApiService } from '../core/services/backend-api.service';
import { Usuario } from '../core/models/usuario';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true,
  imports: [ReactiveFormsModule, ]
  
})
export class RegisterComponent {
  registroForm: FormGroup;

  constructor(private fb: FormBuilder, private backendApi: BackendApiService, private router:Router) {
    this.registroForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', Validators.required],
      contrasenia: ['', Validators.required],
      direccion: ['', Validators.required],
      telefono: ['', Validators.required],
    });
  }

  registrarCliente() {
    const usuario: Usuario = this.registroForm.value;
    console.log(usuario);
    this.backendApi
      .registrarCliente(usuario)
      .subscribe(
        {
          next: (response: any) => {
            console.log('Registro exitoso', response);
            this.router.navigate(['/login'])
          },
          
          error: (error: any) => {
            console.error('Error en el registro', error);
          }
        }
      );
  }
}
