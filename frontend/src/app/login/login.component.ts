import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { BackendApiService } from '../core/services/backend-api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  loginForm: FormGroup

  constructor(private fb:FormBuilder, private api: BackendApiService){
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      contrasenia:['',Validators.required]
    })
  }

  loginCliente() {
    const values = this.loginForm.value;
    const email = values.email;
    const contrasenia = values.contrasenia;
    console.log(email, contrasenia )
  
    this.api.loginCliente(email, contrasenia).subscribe({
      next: (response: any) => {
       
        console.log('Login Exitoso', response);
        // Aquí puedes redirigir al usuario a otra página
      },
      error: (error: any) => {
        console.error('Error en el login', error);
      }
    });
  }
  
}
