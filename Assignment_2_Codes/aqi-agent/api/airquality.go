package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"goaqiagent/models"
	"net/http"
)

func GetAQI(lat, lng float64, apiKey string) (int, error) {
	url := fmt.Sprintf(
		"https://airquality.googleapis.com/v1/currentConditions:lookup?key=%s",
		apiKey,
	)

	requestBody := struct {
		Location struct {
			Latitude  float64 `json:"latitude"`
			Longitude float64 `json:"longitude"`
		} `json:"location"`
	}{}

	requestBody.Location.Latitude = lat
	requestBody.Location.Longitude = lng

	jsonBody, err := json.Marshal(requestBody)
	if err != nil {
		return 0, err
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonBody))
	if err != nil {
		return 0, err
	}

	req.Header.Set("Content-type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	var result models.AQIResponse
	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		return 0, err
	}

	return result.Indexes[0].AQI, nil
}
