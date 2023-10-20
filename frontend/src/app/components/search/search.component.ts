import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { SearchService } from '../../services/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  result: any = null;
  searchForm!: FormGroup;

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {
    this.searchForm = new FormGroup({
      query_data: new FormControl("")
    });
  }

  onSubmit(): void {
    const queryControl = this.searchForm.get('query_data');
    if (queryControl) {
      const queryData = queryControl.value;
      this.searchService.search(queryData).subscribe({
        next: data => {
          console.log('Received data:', data);
          this.result = data;
        },
        error: error => console.error('An error occurred', error)
      });
      
    }
  }
}
