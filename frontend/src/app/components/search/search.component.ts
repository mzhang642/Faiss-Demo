import { Component, OnInit } from '@angular/core';
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
        this.autocompleteOptions = data.matches || []; // Directly use the 'matches' structure
      },
      error: error => console.error('An error occurred', error)
    });
  }
  

  onOptionSelected(event: any): void {
    const selectedName = event.option.value;
    const selectedOption = this.autocompleteOptions.find(option => option.name === selectedName);
    const selectedIndex = selectedOption ? selectedOption.index : null;

    if (selectedIndex !== null) {
        this.searchService.search(selectedIndex).subscribe({
          next: data => {
            this.result = data;
          },
          error: error => console.error('An error occurred', error)
        });
    }
}


}
