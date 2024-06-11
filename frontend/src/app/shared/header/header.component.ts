import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  standalone: true
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    const burger = document.querySelector('.burger') as HTMLElement; // Cast a HTMLElement
    const navbar = document.querySelector('.navbar') as HTMLElement; // Cast a HTMLElement

    burger.addEventListener('click', () => {
      navbar.classList.toggle('active');
    });
  }

}
