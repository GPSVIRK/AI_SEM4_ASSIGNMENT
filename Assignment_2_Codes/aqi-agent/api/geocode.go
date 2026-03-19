package api

import (
	"encoding/json"
	"fmt"
	"goaqiagent/models"
	"net/http"
	"net/url"
)

func GetCoordinates(state, country, apiKey string) (float64, float64, error) {

	address := fmt.Sprintf("%s, %s", state, country)
	encodeAddress := url.QueryEscape(address)

	url := fmt.Sprintf(
		"https://geocode.googleapis.com/v4beta/geocode/address/%s",
		encodeAddress,
	)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return 0, 0, err
	}

	req.Header.Set("X-Goog-Api-Key", apiKey)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return 0, 0, err
	}

	defer resp.Body.Close()

	var result models.GeocodeResponse

	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		return 0, 0, err
	}

	if len(result.Results) == 0 {
		return 0, 0, fmt.Errorf("location not found")
	}

	lat := result.Results[0].Location.Latitude
	lng := result.Results[0].Location.Longitude

	return lat, lng, nil

}
