import { Routes } from "@angular/router";
import { HomeComponent } from "./home/home.component";
import { ProductosComponent } from "./productos/productos.component";

export const PAGES_ROUTES: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path:'productos',
        component:ProductosComponent
    }
]