import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { BackendApiService } from '../../core/services/backend-api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loginForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private api: BackendApiService,
    private toastr: ToastrService
  ) {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      contrasenia: ['', Validators.required],
    });
  }

  get email() {
    return this.loginForm.controls['email'];
  }

  get contrasenia() {
    return this.loginForm.controls['contrasenia'];
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
  regexEmail = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;

  loginCliente() {
    if (!this.loginForm.valid) {
      this.showError('El formulario no es valido');
    } else if (!this.regexEmail.test(this.email.value)) {
      this.showError('Ingrese un email valido');
    } else if (!this.regexContrasenia.test(this.contrasenia.value)) {
      this.showError('la contraseña no cumple con el formsto pedido');
    } else {
      const values = this.loginForm.value;
      const email = values.email;
      const contrasenia = values.contrasenia;
      console.log(email, contrasenia);

      this.api.loginCliente(email, contrasenia).subscribe({
        next: (response: any) => {
          console.log('Login Exitoso', response);
          this.showSuccess('Sesion iniciada correctamente')
        },
        error: (error: any) => {
          console.error('Error en el login', error);
          this.showError('Error al iniciar sesion')
        },
      });
    }
  }

  mostrarContrasenia() {
    // Asegúrate de que el elemento existe y es un HTMLInputElement
    const inputContrasenia = document.getElementById(
      'contrasenia'
    ) as HTMLInputElement | null;
    const icon = document.querySelector('.icon') as HTMLElement | null;

    if (!inputContrasenia || !icon) {
      return;
    }

    if (inputContrasenia.type === 'password') {
      inputContrasenia.type = 'text';
      icon.innerHTML = `
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-eye" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round" (click)="mostrarContrasenia()>
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
  <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
</svg>      `;
    } else {
      inputContrasenia.type = 'password';
      icon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-eye-closed" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round" (click)="mostrarContrasenia()>
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M21 9c-2.4 2.667 -5.4 4 -9 4c-3.6 0 -6.6 -1.333 -9 -4" />
  <path d="M3 15l2.5 -3.8" />
  <path d="M21 14.976l-2.492 -3.776" />
  <path d="M9 17l.5 -4" />
  <path d="M15 17l-.5 -4" />
</svg>
      `;
    }
  }
}
