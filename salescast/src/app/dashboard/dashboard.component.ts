import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { HttpClient } from '@angular/common/http';
import { NgForm } from '@angular/forms';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  data = {
    "periodicity": '',
    "periods": '',
    "fileInput": ''
  }
  onSubmit(form: NgForm) {
    const formData = new FormData();
    formData.append('periodicity', form.value.periodicity);
    formData.append('periods', form.value.periods);
    formData.append('fileInput', this.data.fileInput)
    this.http.post('http://127.0.0.1:5000/process-data', formData).subscribe({
      next: (value) => {
        console.log(value)
        //@ts-ignore
        const base64ImageData = value.img
        // Convert the base64-encoded data to an image
        const img = new Image();
        img.src = `data:image/png;base64,${base64ImageData}`;
        let ig = (document.getElementById("result") as HTMLImageElement)
        ig.src = `data:image/png;base64,${base64ImageData}`;
        ig.removeAttribute('hidden')
      },
      complete: () => {
        console.log('Form submitted successfully');
        // handle response from server
      },
      error: (error) => {
        console.error('Error submitting form', error);
        // handle error from server
      },
    }
    );
  }

  constructor(private auth: AuthService, private http: HttpClient) { }

  user = { localId: "someid", displayName: "somename" };
  ngOnInit(): void {
    this.auth.canAccess();
    if (this.auth.isAuthenticated()) {
      //call user details service
      this.auth.detail().subscribe({
        next: data => {
          this.user.localId = data.users[0].localId;
          this.user.displayName = data.users[0].displayName;
        }
      })
    }
  }
  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.data.fileInput = file;
  }
}
