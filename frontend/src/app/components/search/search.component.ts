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
  fuzzyResults: any = null;
  searchForm!: FormGroup;

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {
    this.searchForm = new FormGroup({
      query_data: new FormControl(""),
      query_text: new FormControl('')  // You can keep this for now
    });
  }

  onTextInput(): void {
    const textControl = this.searchForm.get('query_data');
    if (textControl && textControl.value && isNaN(textControl.value)) {
      console.log("Performing Fuzzy Search");
      this.searchService.fuzzySearch(textControl.value).subscribe({
        next: data => {
          console.log("Fuzzy Results: ", data);
          this.fuzzyResults = data.matches;
        },
        error: error => console.error('An error occurred', error)
      });
    }
  }

  onSelectIndex(event: any): void {
    console.log("Dropdown index selected");
    const selectedIndex = event.target.value;
    this.searchService.search(selectedIndex).subscribe({
      next: data => {
        console.log("Search API Results: ", data);
        this.result = data;
      },
      error: error => console.error('An error occurred', error)
    });
  }

  onSubmit(): void {
    const queryControl = this.searchForm.get('query_data');
    if (queryControl && queryControl.value && !isNaN(queryControl.value)) {
      console.log("Submitting direct index search");
      const queryData = queryControl.value;
      this.searchService.search(queryData).subscribe({
        next: data => {
          console.log("Search API Results: ", data);
          this.result = data;
        },
        error: error => console.error('An error occurred', error)
      });
      
    }
  }
}
