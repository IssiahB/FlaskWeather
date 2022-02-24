from flask import Flask, render_template, request
import requests

app = Flask('Weather App')

class WeatherRequest:
	def __init__(self, location=None):
		if location is None:
			raise ValueError("No location given")

		self.loc = location
		self.base_url = 'http://api.openweathermap.org/data/2.5/weather?'
		self.api_key = 'API KEY HERE'
		self.unit_type = 'units=imperial'
		self.app_id = 'appid='+self.api_key
		self.query = 'q='+location
		self.full_url = self.base_url + self.app_id + '&' +self.unit_type+ '&' + self.query
		self.isValid = self._searchData()

	def _searchData(self):
		try:
			self.request_data = requests.get(self.full_url, allow_redirects=False).json()
			return True
		except:
			return False

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route('/search')
def search():
	loc = request.args.get('location')
	requ = WeatherRequest(loc)
	if requ.isValid:
		return render_template('view.html', task=requ)
	else:
		return '<h1 style="color:red;">Invalid Location</h1>'

if __name__ == "__main__":
	app.run(debug=True)
	