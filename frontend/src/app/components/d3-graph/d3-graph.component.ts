// d3-graph.component.ts
import { Component, Input, OnInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import { SearchService } from '../../services/search.service';
import * as d3 from 'd3';
import { Subscription } from 'rxjs';

interface Node extends d3.SimulationNodeDatum {
  id: string;
  // Define other properties your nodes may have
}

interface Link extends d3.SimulationLinkDatum<Node> {
  source: Node;
  target: Node;
  // Define properties your links may have, like 'source' and 'target' which are required
}

interface GraphData {
  nodes: Node[];
  links: Link[];
}

@Component({
  selector: 'app-d3-graph',
  template: '<div #graphContainer></div>',
  styleUrls: ['./d3-graph.component.css']
})
export class D3GraphComponent implements OnInit, OnDestroy {
  @Input() graphData: any; // Make sure this is decorated with @Input()
  @ViewChild('graphContainer', { static: true }) private graphContainer!: ElementRef;
  private graphSubscription!: Subscription;

  constructor(private searchService: SearchService) {}

  ngOnInit() {
    this.graphSubscription = this.searchService.graphData$.subscribe(graphData => {
      console.log('Received graphData:', graphData);  
      if (graphData) {
        this.renderGraph(graphData as GraphData);
      }
    });
  }

  private renderGraph(graphData: GraphData): void {
    // Clear the existing graph
    d3.select(this.graphContainer.nativeElement).selectAll('*').remove();

    // Set up the simulation and add forces
    // Now ensure that the id accessor function for forceLink properly returns the identifier
    let simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink<Node, Link>(graphData.links).id(d => d.id))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(this.graphContainer.nativeElement.offsetWidth / 2, this.graphContainer.nativeElement.offsetHeight / 2));

    // Create the link lines
    let link = d3.select(this.graphContainer.nativeElement).append('svg')
      .attr('width', this.graphContainer.nativeElement.offsetWidth)
      .attr('height', this.graphContainer.nativeElement.offsetHeight)
      .selectAll('line')
      .data(graphData.links)
      .enter().append('line')
      .attr('stroke-width', 2)
      .style('stroke', 'grey');

    // Create the node circles
    let node = d3.select(this.graphContainer.nativeElement).append('svg')
      .attr('width', this.graphContainer.nativeElement.offsetWidth)
      .attr('height', this.graphContainer.nativeElement.offsetHeight)
      .selectAll('circle')
      .data(graphData.nodes)
      .enter().append('circle')
      .attr('r', 5)
      .style('fill', 'blue');

    // Drag functionality for nodes
    const drag = (simulation: d3.Simulation<Node, undefined>) => {
      function dragstarted(event: d3.D3DragEvent<SVGCircleElement, Node, Node>) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      
      function dragged(event: d3.D3DragEvent<SVGCircleElement, Node, Node>) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event: d3.D3DragEvent<SVGCircleElement, Node, Node>) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return d3.drag<SVGCircleElement, Node>()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended);
    };

    node.call(drag(simulation) as any); // Cast as any if there are still type issues

    // Update positions each tick of the simulation
    simulation.on('tick', () => {
      link
          .attr('x1', (d) => (d as Link).source.x!)
          .attr('y1', (d) => (d as Link).source.y!)
          .attr('x2', (d) => (d as Link).target.x!)
          .attr('y2', (d) => (d as Link).target.y!);

      node
          .attr('cx', d => (d as Node).x!)
          .attr('cy', d => (d as Node).y!);
    });

    console.log('Rendering graph with data:', graphData); // Add for debugging
  }

  ngOnDestroy() {
    if (this.graphSubscription) {
      this.graphSubscription.unsubscribe();
    }
  }
}
