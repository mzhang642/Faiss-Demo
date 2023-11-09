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
  graphData: any = null;  

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
            // Update the result with the new data
            this.result = data;
            // Transform the data to graph format.
            const graphData = this.transformToGraphData(data); 
            // Update the BehaviorSubject with the new graph data.
            this.searchService.updateGraphData(graphData); 
          },
          error: error => console.error('An error occurred', error)
        });
    }
  }

  // Function to transform your result JSON into a format suitable for D3's force-directed graph
  private transformToGraphData(data: any): any {
    const nodes: { id: string, group: number, data: any }[] = [];
    const links: { source: string, target: string, value: number }[] = [];
  
    // Add the central node (input food)
    const centralFood = data['similar foods'][0]; // Assuming first is always the input food
    nodes.push({ id: centralFood.description, group: 1, data: centralFood });
  
    // Add similar foods as nodes and their distances as links
    data['similar foods'].forEach((food: any, i: number) => {
      if (i > 0) { // Skip the first one since it's the central food
        nodes.push({ id: food.description, group: 2, data: food });
  
        // Now, create links with the distance as the value
        const distance = data.distances[0][i];
        links.push({
          source: centralFood.description,
          target: food.description,
          value: distance
        });
      }
    });
  
    return { nodes, links };
  
  }  

}
