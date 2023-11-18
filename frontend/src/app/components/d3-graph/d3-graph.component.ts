import { Component, Input, OnInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import { SearchService } from '../../services/search.service';
import * as d3 from 'd3';
import { Subscription } from 'rxjs';

interface Node extends d3.SimulationNodeDatum {
  id: string;
  group: number;
  data: any; // Define other properties your nodes may have
}

interface Link extends d3.SimulationLinkDatum<Node> {
  source: Node;
  target: Node;
  value: number; // Define properties your links may have, like 'source' and 'target' which are required
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

  constructor(private searchService: SearchService) { }

  ngOnInit() {
    this.graphSubscription = this.searchService.graphData$.subscribe(graphData => {
      console.log('Received graphData:', graphData);
      if (graphData) {
        this.renderGraph(graphData as GraphData);
      }
    });
  }

  private renderGraph(graphData: GraphData): void {
    d3.select(this.graphContainer.nativeElement).selectAll('*').remove();

    const linkValueByNodeId = new Map<string, number>();
    graphData.links.forEach(link => {
      const targetId = typeof link.target === 'object' ? link.target.id : link.target;
      linkValueByNodeId.set(targetId, link.value);
    });

    const colorScale = d3.scaleLinear<string>()
      .domain(d3.extent(graphData.links, d => d.value) as [number, number])
      .range(['lightblue', 'darkblue']);

    const sizeScale = d3.scaleLinear<number>()
      .domain(d3.extent(graphData.links, d => d.value) as [number, number])
      .range([5, 15]);

    const svg = d3.select(this.graphContainer.nativeElement).append('svg')
      .attr('width', this.graphContainer.nativeElement.offsetWidth)
      .attr('height', this.graphContainer.nativeElement.offsetHeight);

    let simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink<Node, Link>(graphData.links).id(d => d.id))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(
        parseFloat(svg.attr('width')) / 2, 
        parseFloat(svg.attr('height')) / 2
      ));

    let link = svg.selectAll('line')
      .data(graphData.links)
      .enter().append('line')
      .attr('stroke-width', 2)
      .style('stroke', 'grey');

    let node = svg.selectAll('circle')
      .data(graphData.nodes)
      .enter().append('circle')
      .attr('r', d => {
        if (d.group === 1) {
          return 20;  // Fixed size for central node (group 1)
        } else {
          const linkValue = linkValueByNodeId.get(d.id);
          return linkValue ? sizeScale(linkValue) : 5;
        }
      })
      .style('fill', d => d.group === 1 ? 'green' : colorScale(linkValueByNodeId.get(d.id) ?? 0));

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

    node.call(drag(simulation) as any); 

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
  }

  ngOnDestroy() {
    if (this.graphSubscription) {
      this.graphSubscription.unsubscribe();
    }
  }
}
