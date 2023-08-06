#weather_forecast.py
import requests , pytz, datetime, math
from quickchart import QuickChart
from geopy.geocoders import Nominatim


class WeatherChart:
	def __init__(self, map_key, tz_location='Asia/Singapore' ) :
		self.apikey = map_key 
		self.tz = pytz.timezone( tz_location )

	def get_full_weather_data_by_location(self, lat, long):
		url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&appid={self.apikey}&units=metric'
		r = requests.get(url)
		return r.json()
		if r.status_code == 200:
			return r.json()
		else:
			return None

	def get_forecast(self, lat, long):
		weather = self.get_full_weather_data_by_location(lat, long)

		forecast = {}
		for index in range( 0, 8):
			local_time = datetime.datetime.fromtimestamp( weather['daily'][index]['dt'] , tz=self.tz )
			str_time = local_time.strftime( '%a %Y-%m-%d' )
			forecast[ str_time ] =  {
										'temp': round(weather['daily'][index]['temp']['day'],1),
										'temp_min': weather['daily'][index]['temp']['min'],
										'temp_max': weather['daily'][index]['temp']['max'],
										'wind_speed': weather['daily'][index]['wind_speed'],
										'humidity': weather['daily'][index]['humidity']
									}

		return forecast

	def get_forecast_chart_image_by_loc( self, loc_string , output_file):
		geolocator = Nominatim(user_agent="pubs_01")
		location = geolocator.geocode( loc_string )
		if location: return self.get_forecast_chart_image( location.latitude, location.longitude, output_file )

		return None


	def get_forecast_chart_image( self, lat, long , output_file):
		qc = QuickChart() 
		qc.width = 500 #set width and height of chart in pixels
		qc.width = 500

		labels = []	#Declare to hold the x-axis tick labels
		weather_readings = []  #get the data labels
		
		forecast = self.get_forecast( lat, long)
		
		for item_key in forecast.keys():
			labels.append( item_key )
			weather_readings.append( forecast[ item_key ]['temp'] )
		
		qc.config = self._get_forecast_chart_image_config( labels, weather_readings)
		print( qc.get_short_url() ) 	#Print out the chart URL
		qc.to_file( output_file )	#Save to a file
	
	def _get_forecast_chart_image_config(self, labels, weather_readings ):
		min, max = self._get_min_max_tick_item( weather_readings, 2)

		return { 'type': 'line',
				'data': { 'labels':  [''] + labels +[''],
				'datasets': [ { 
								'backgroundColor': 'rgb(255, 99, 132)', 
								'data':  [None] + weather_readings ,
								'lineTension': 0.4,
								'fill': False,
								} ],
						},
				'options': {
							'title': { 'display': True,  
										'text': '7-Day Weather Forecast' }, 
							'legend': { 'display': False}, 
							'scales': { 'yAxes': [ { 
														'scaleLabel':  { 
																		'display': True, 
																		'labelString': 'Temperature Degrees Celcius' 
																		} 
													} ]
										},
							'plugins': { 
											'datalabels': {
															'display': True,
															'align': 'bottom',
															'backgroundColor': '#ccc',
															'borderRadius': 3
														},
										},
							'scales': {  'yAxes': [{
											'scaleLabel': {
											'display': True,
											'labelString': 'Temperature Degrees Celcius'
											},
											'ticks': {
											'min': min,
											'max': max,
											'stepSize': 2  
											}
										}]
										}

							},
					} 
	
	def _get_min_max_tick_item(self, weather_readings, divisor):

		#First find the min and max values
		min = 1000
		max = 0
		for reading in weather_readings:
			if reading < min: min = reading
			if reading > max: max = reading

		#Round the values with gaps in between
		min = math.floor(min * 0.8 / divisor)  * divisor
		max = math.ceil(max * 1.2 / divisor)  * divisor
 
		return min, max