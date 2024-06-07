import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, { 
  providers: [
    importProvidersFrom(ReactiveFormsModule),
    provideHttpClient(),
    provideRouter(routes)
  ]
})
.catch(err => console.error(err));

