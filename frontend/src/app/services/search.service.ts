import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private apiUrl = 'http://localhost:5000/api/search';
  private fuzzyApiUrl = 'http://localhost:5000/api/fuzzy_matching';
  private graphDataSubject = new BehaviorSubject<any>(null);
  public graphData$ = this.graphDataSubject.asObservable();

  constructor(private http: HttpClient) { }

  // <any>: This is a type parameter that specifies the type of data that the observable emits. 
  fuzzySearch(queryText: string): Observable<any> {
    return this.http.post<any>(this.fuzzyApiUrl, { 'query_data': queryText });
  }
  search(query_data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, { 'query_data': query_data });
  }
  updateGraphData(data: any) {
    this.graphDataSubject.next(data);
  }
}
