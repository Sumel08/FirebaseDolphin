import {Component, OnDestroy, AfterViewInit} from '@angular/core';
import {AngularFirestore} from 'angularfire2/firestore';
import {Observable} from 'rxjs';
import {AmChart, AmChartsService} from '@amcharts/amcharts3-angular';
import {ChartsService} from '../services/charts';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnDestroy, AfterViewInit {

  private temperature_chart: AmChart;
  private humidity_chart: AmChart;

  temperature_data: Observable<any[]>;
  humidity_data: Observable<any[]>;

  constructor(db: AngularFirestore,
              private AmCharts: AmChartsService,
              private chartsService: ChartsService) {

    // this.temperature_data = db.collection('temp').valueChanges();

    db.collection('temperature').valueChanges().subscribe(
      items => {
        this.AmCharts.updateChart(this.temperature_chart, () => {
          this.temperature_chart.dataProvider = items;
        });
      }
    );

    db.collection('humidity').valueChanges().subscribe(
      items => {
        this.AmCharts.updateChart(this.humidity_chart, () => {
          this.humidity_chart.dataProvider = items;
        });
      }
    );
  }

  ngAfterViewInit() {
    this.temperature_chart = this.chartsService.linearChart(
      'Temperature',
      'temperature_chart',
      this.temperature_data
    );

    this.humidity_chart = this.chartsService.linearChart(
      'Humedad',
      'humidity_chart',
      this.humidity_data
    );
  }

  ngOnDestroy() {
    if (this.temperature_chart) {
      this.AmCharts.destroyChart(this.temperature_chart);
    }

    if (this.humidity_chart) {
      this.AmCharts.destroyChart(this.humidity_chart);
    }
  }
}
