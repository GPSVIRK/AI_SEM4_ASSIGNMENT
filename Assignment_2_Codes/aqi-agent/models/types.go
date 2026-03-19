package models

type GeocodeResponse struct {
	Results []struct {
		Location struct {
			Latitude  float64 `json:"latitude"`
			Longitude float64 `json:"longitude"`
		} `json:"location"`
	} `json:"results"`
}

type AQIResponse struct {
	Indexes []struct {
		Code string `json:"code"`
		AQI  int    `json:"aqi"`
	} `json:"indexes"`
}
