import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private apiUrl = 'http://localhost:5000/api/search';
  private fuzzyApiUrl = 'http://localhost:5000/api/fuzzy_matching';

  constructor(private http: HttpClient) { }

  // search.service.ts
  fuzzySearch(queryText: string): Observable<any> {
    return this.http.post<any>(this.fuzzyApiUrl, { 'query_data': queryText });
  }
  search(query_data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, { 'query_data': query_data });
  }
}
