import {AmChartsService} from '@amcharts/amcharts3-angular';
import {Injectable} from '@angular/core';

@Injectable()
export class ChartsService {

  constructor(private AmCharts: AmChartsService) {

  }

  linearChart(title, container, dataProvider) {
    return this.AmCharts.makeChart(container, {
      'type': 'serial',
      'categoryField': 'date',
      'dataDateFormat': 'YYYY-MM-DD HH:NN:SS',
      'categoryAxis': {
        'minPeriod': 'ss',
        'parseDates': true
      },
      'chartCursor': {
        'enabled': true,
        'categoryBalloonDateFormat': 'JJ:NN:SS'
      },
      'chartScrollbar': {
        'enabled': true
      },
      'trendLines': [],
      'graphs': [
        {
          'bullet': 'round',
          'id': 'temperature',
          'title': 'Temperature',
          'valueField': 'value'
        }
      ],
      'guides': [],
      'valueAxes': [
        {
          'id': 'ValueAxis-1',
          'title': 'Axis title'
        }
      ],
      'allLabels': [],
      'balloon': {},
      'legend': {
        'enabled': true,
        'useGraphSettings': true
      },
      'titles': [
        {
          'id': 'Title-1',
          'size': 15,
          'text': title
        }
      ],
      'dataProvider': dataProvider
    });
  }
}
