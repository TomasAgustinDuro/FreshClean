import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
  AbstractControl,
} from '@angular/forms';
import { BackendApiService } from '../../core/services/backend-api.service';
import { Usuario } from '../../core/models/usuario';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true,
  imports: [ReactiveFormsModule],
})
export class RegisterComponent {
  registroForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authAPI: AuthService,
    private router: Router,
    private toastr: ToastrService
  ) {
    this.registroForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', Validators.required],
      contrasenia: ['', Validators.required],
      direccion: ['', Validators.required],
      telefono: ['', Validators.required],
    });
  }

  get Email() {
    return this.registroForm.controls['email'];
  }

  get Contrasenia() {
    return this.registroForm.controls['contrasenia'];
  }

  get first_name() {
    return this.registroForm.controls['nombre'];
  }

  get last_name() {
    return this.registroForm.controls['apellido'];
  }

  get direccion() {
    return this.registroForm.controls['direccion'];
  }

  get telefono() {
    return this.registroForm.controls['telefono'];
  }

  showSuccess(message = '') {
    this.toastr.success(message, '', {
      progressBar: true,
      timeOut: 3000,
    });
  }

  showError(message = '') {
    this.toastr.error(message, '', {
      progressBar: true,
      timeOut: 3000,
    });
  }
  regexContrasenia = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  regexNombre = /^[A-Za-záéíóúüñÁÉÍÓÚÜÑ\s]+$/;
  regexTfn = /^\d{10}$/;
  regexEmail = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;

  registrarCliente() {
    if (!this.registroForm.valid) {
      this.showError('El formulario no es valido');
    } else if (!this.regexContrasenia.test(this.Contrasenia.value)) {
      this.showError(
        'La contraseña debe contener 8 caracteres minimo, 1 mayuscula, 1 numero y 1 signo'
      );
    } else if (
      !this.regexNombre.test(this.first_name.value) &&
      !this.regexNombre.test(this.last_name.value)
    ) {
      this.showError('El nombre y el apellido solo deben contener letras.');
    } else if (!this.regexEmail.test(this.Email.value)) {
      this.showError('Ingrese un email.valido');
    } else if (!this.regexTfn.test(this.telefono.value)) {
      this.showError('El telefono tiene un formato incorrecto');
    } else {
      const usuario: Usuario = this.registroForm.value;
      console.log(usuario);
      this.authAPI.registrarCliente(usuario).subscribe({
        next: (response: any) => {
          console.log('Registro exitoso', response);
          this.router.navigate(['/login']);
        },

        error: (error: any) => {
          console.error('Error en el registro', error);
        },
      });
    }
  }

  mostrarContrasenia() {
    const inputContrasenia = document.querySelector(
      '#contrasenia'
    ) as HTMLInputElement | null;
    const icon = document.querySelector('.icon') as HTMLElement | null;

    if (!inputContrasenia || !icon) {
      return;
    }

    if (inputContrasenia.type === 'password') {
      inputContrasenia.type = 'text';
      icon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-eye" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round" (click)="mostrarContrasenia()">
          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
          <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
          <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
        </svg>`;
    } else {
      inputContrasenia.type = 'password';
      icon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-eye-closed" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round" (click)="mostrarContrasenia()">
          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
          <path d="M21 9c-2.4 2.667 -5.4 4 -9 4c-3.6 0 -6.6 -1.333 -9 -4" />
          <path d="M3 15l2.5 -3.8" />
          <path d="M21 14.976l-2.492 -3.776" />
          <path d="M9 17l.5 -4" />
          <path d="M15 17l-.5 -4" />
        </svg>`;
    }
  }
}
