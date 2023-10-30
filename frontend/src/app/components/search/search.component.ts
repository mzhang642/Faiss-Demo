import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { SearchService } from '../../services/search.service';

@Component({
    selector: 'app-search',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  queryText: string = '';
  result: any = null;
  autocompleteOptions: any[] = [];

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {}

  fetchAutocompleteOptions(): void {
    if (!this.queryText) {
      this.autocompleteOptions = [];
      return;
    }

    this.searchService.fuzzySearch(this.queryText).subscribe({
      next: data => {
        this.autocompleteOptions = data.matches || [];
      },
      error: error => console.error('An error occurred', error)
    });
  }

  onOptionSelected(event: any): void {
    const selectedValue = event.option.value;
    this.searchService.search(selectedValue).subscribe({
      next: data => {
        this.result = data;
      },
      error: error => console.error('An error occurred', error)
    });
  }
}
